import logging
from typing import Generator, List, Union
from urllib.parse import urljoin
from pathlib import Path

from transformers import AutoTokenizer
from langchain_text_splitters import RecursiveCharacterTextSplitter
import opensearchpy
from fastapi.exceptions import HTTPException
from starlette.datastructures import UploadFile
from google.cloud import storage
from langchain_core.documents.base import Document
from langchain.vectorstores.base import VectorStore
from langchain_community.document_loaders import PDFPlumberLoader
from tenacity import retry, stop_after_attempt, wait_fixed

from tock_genai_core.models.database import DBSetting
from tock_genai_core.models.embedding import EMSetting
from tock_genai_core.models.embedding.provider import EMProvider
from tock_genai_core.routes.responses import IngestionResponse
from tock_genai_core.routes.requests import RawContent
from tock_genai_core.services.langchain.factory.db_factory import (
    get_vector_db_factory,
)
from tock_genai_core.services.database.postgres import add_document_to_relational_db


logger = logging.getLogger(__name__)

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


def divide_chunks(documents: list[Document], n: int) -> Generator[list[Document], None, None]:
    """
    Divides a list of documents into chunks of a specified size.

    This function yields chunks of the provided list of documents, where each chunk contains up to `n` documents.

    Parameters
    ----------
    documents : list[Document]
        The list of `Document` instances to be divided into chunks.

    n : int
        The size of each chunk. Determines how many documents will be included in each yielded chunk.

    Returns
    -------
    Generator[list[Document], None, None]
        A generator that yields chunks of documents, each containing up to `n` documents.

    """
    for i in range(0, len(documents), n):
        yield documents[i : i + n]


@retry(wait=wait_fixed(60), stop=stop_after_attempt(6))
def ingest_document(
    vector_store: VectorStore,
    documents: list[Document],
    space_type: str = None,
    index: str = None,
):
    """
    Ingests a list of documents into the specified vector store.

    This function attempts to add documents to the vector store, retrying up to 6 times with a 60-second
    wait between attempts in case of a failure.

    Parameters
    ----------
    vector_store : VectorStore
        The vector store instance where the documents will be ingested.

    documents : list[Document]
        A list of `Document` instances to be ingested into the vector store.

    space_type : str, optional
        The space type for the vector store, used for certain vector databases like OpenSearch. Defaults to `None`.

    index : str, optional
        The index name within the vector store where the documents will be stored. Defaults to `None`.

    Returns
    -------
    None

    Raises
    ------
    opensearchpy.exceptions.RequestError
        If an error occurs during the request to the vector store.

    opensearchpy.helpers.errors.BulkIndexError
        If a bulk index error occurs during document ingestion.
    """
    try:
        vector_store.add_documents(documents, index_name=index, space_type=space_type)
    except (
        opensearchpy.exceptions.RequestError,
        opensearchpy.helpers.errors.BulkIndexError,
    ):
        logger.exception("Error during document ingestion")


def save_artefact_in_storage(bucket_name: str, folder: str, file: UploadFile) -> str:
    """
    Saves a file in a GCS bucket.

    Parameters
    ----------
    bucket_name : str
    folder : str
    file : UploadFile

    Returns
    -------
    Artefact path.
    """
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(urljoin(folder, file.filename))
    blob.upload_from_file(file_obj=file.file, rewind=True)
    return blob.path


def execute_ingest_chain(
    content: Union[list[RawContent], list[UploadFile]],
    chunk_size: int,
    chunk_overlap: int,
    em_settings: EMSetting,
    db_settings: DBSetting,
    metadata: dict,
) -> IngestionResponse:
    """
    Executes the ingestion process for a list of raw content or uploaded files, splits the content into chunks,
    and stores it in both a vector store and a relational database.

    Parameters
    ----------
    content : Union[list[RawContent], list[UploadFile]]
        A list of raw content or uploaded files to be ingested. Each item can either be an instance of `RawContent`
        (containing content and metadata) or `UploadFile` (representing a file to load and process).

    chunk_size : int
        The maximum size for each chunk of text when splitting the content.

    chunk_overlap : int
        The overlap between chunks to ensure continuity of information between them.

    em_settings : EMSetting
        The settings related to the embedding model, including the provider to be used for text splitting and chunking.

    db_settings : DBSetting
        The settings related to the database, including the vector database and relational database configuration.

    metadata : dict
        A dictionary of additional metadata to be associated with the ingested documents.

    Returns
    -------
    IngestionResponse
        An object containing the filenames of the ingested documents.
    """
    documents: List[Document] = []
    filenames: List[str] = []

    for c in content:
        unsplitted_documents = []

        if isinstance(c, UploadFile):
            logger.info(f"Loading file {c.filename}")
            file_path = Path(c.filename)

            try:
                with file_path.open("wb") as f:
                    f.write(c.file.read())

                loader = PDFPlumberLoader(str(file_path))
                unsplitted_documents = loader.load()
                filenames.append(c.filename)
            except Exception as e:
                logger.error(f"Error loading file {c.filename}: {e}")
                continue
            finally:
                file_path.unlink(missing_ok=True)
        elif isinstance(c, RawContent):
            unsplitted_documents = [Document(page_content=content, metadata=c.metadata) for content in c.content]
            filenames.append(c.name)

        if chunk_size:
            splitter = None

            if em_settings.provider == EMProvider.BloomZ:
                tokenizer = AutoTokenizer.from_pretrained("cmarkea/bloomz-3b-retriever-v2")
                splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
                    tokenizer, chunk_size=chunk_size, chunk_overlap=chunk_overlap
                )

            elif em_settings.provider == EMProvider.OpenAI:
                # You can check the encoding name at :
                # https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
                splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                    encoding_name="cl100k_base", chunk_size=chunk_size, chunk_overlap=chunk_overlap
                )

            elif em_settings.provider == EMProvider.Vllm:
                tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-7B-Instruct-AWQ")
                splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
                    tokenizer, chunk_size=chunk_size, chunk_overlap=chunk_overlap
                )
            else:
                raise HTTPException(status_code=422, detail=f"Unsupported embedding provider : {em_settings.provider}")

            documents.extend(splitter.split_documents(unsplitted_documents))
        else:
            documents.extend(unsplitted_documents)

    if metadata:
        for doc in documents:
            doc.metadata.update(metadata)

    vector_store = get_vector_db_factory(db_settings=db_settings, em_settings=em_settings).get_vector_store()

    chunks = divide_chunks(documents, 16)  # send chunks 16 by 16 to vector db

    for documents in chunks:
        ingest_document(vector_store, documents, space_type=em_settings.space_type, index=db_settings.index)

    add_document_to_relational_db(db_settings=db_settings, metadata=metadata, filenames=filenames)

    return IngestionResponse(filename=filenames)
