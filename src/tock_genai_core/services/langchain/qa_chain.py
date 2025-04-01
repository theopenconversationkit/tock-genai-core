import json
import logging

from langchain_core.runnables import RunnableParallel

from tock_genai_core.routes.requests import requests
from tock_genai_core.routes.responses import responses
from tock_genai_core.services.langchain.chain_utils import get_base_search_kwargs
from tock_genai_core.services.langchain.factory.db_factory import (
    get_vector_db_factory,
)
from tock_genai_core.services.langchain.rag_chain import get_handlers, add_compressor
from tock_genai_core.services.gs_image import download_gcs_image

logger = logging.getLogger(__name__)

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


def execute_qa_chain(query: requests.SearchRequest) -> responses.SearchResponse:
    """
    Executes a question-answering chain using a vector store and document retriever.

    This function performs a vector similarity search using the provided query, retrieves relevant documents
    from the vector store, and processes them through a question-answering (QA) chain. If necessary, a compressor
    is added to the retriever, and the documents are returned along with optional images.

    Parameters
    ----------
    query : requests.SearchRequest
        The search query containing parameters such as question, language settings, database settings,
        embedding settings, and compressor settings for document retrieval and QA.

    Returns
    -------
    responses.SearchResponse
        The response containing the retrieved documents and trace information, if available.
    """
    handlers = get_handlers(query.langfuse_settings)

    vector_store = get_vector_db_factory(
        db_settings=query.db_settings, em_settings=query.em_settings
    ).get_vector_store()

    search_kwargs = get_base_search_kwargs(query)
    logger.info(f"Running vector similarity search with search_kwargs={json.dumps(search_kwargs)}")
    retriever = vector_store.as_retriever(search_kwargs=search_kwargs)
    if query.compressor_settings:
        retriever = add_compressor(retriever, query.compressor_settings)

    qa_chain = RunnableParallel({"documents": retriever})

    result = qa_chain.invoke(query.question, config={"callbacks": list(handlers.values())})

    documents = []
    for document in result["documents"]:
        image_b64 = None
        if {"bucket", "blob"}.issubset(document.metadata.keys()):
            image_b64 = download_gcs_image(document.metadata["bucket"], document.metadata["blob"])

        documents.append({"page_content": document.page_content, "metadata": document.metadata, "image": image_b64})

    return responses.SearchResponse(
        trace_id=(handlers["langfuse"].get_trace_id() if "langfuse" in handlers else None), documents=documents
    )
