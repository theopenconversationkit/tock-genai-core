import json
from operator import itemgetter
from typing import List, Iterator
import logging

from fastapi import HTTPException
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain.schema.output_parser import StrOutputParser
from langchain.retrievers import ContextualCompressionRetriever
from langchain.schema.runnable import RunnableParallel
from langchain_core.language_models import BaseLanguageModel
from langchain_core.runnables import RunnableSerializable, RunnablePassthrough
from langchain_core.vectorstores import VectorStoreRetriever
from langfuse.callback import CallbackHandler

from tock_genai_core.models.contextual_compressor import BaseCompressorSetting
from tock_genai_core.models.guardrail import BaseGuardrailSetting
from tock_genai_core.models.langfuse.setting import LangfuseSetting
from tock_genai_core.routes.requests import requests
from tock_genai_core.routes.responses import responses
from tock_genai_core.services.langchain.chain_utils import get_base_search_kwargs
from tock_genai_core.services.langchain.factory.llm_factory import get_llm_factory
from tock_genai_core.services.langchain.factory.db_factory import (
    get_vector_db_factory,
)
from tock_genai_core.services.langchain.factory.compressor_factory import (
    get_compressor_factory,
)
from tock_genai_core.services.langchain.factory.guardrail_factory import (
    get_guardrail_factory,
)
from tock_genai_core.services.langfuse.handler import LangfuseHandler
from tock_genai_core.services.gs_image import download_gcs_image

logger = logging.getLogger(__name__)

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


def uniform_itemgetter(*args):
    """
    Returns a function that retrieves specified items from an object.

    Parameters
    ----------
    *args : str or int
        The keys or indices to retrieve from the object.

    Returns
    -------
    function
        A function that, when called with an object, returns a tuple containing the requested items
        if only one argument is provided, or the specified items directly if multiple arguments are given.
    """
    if len(args) != 1:
        return itemgetter(*args)
    return lambda x: (itemgetter(*args)(x),)


def add_compressor(
    retriever: VectorStoreRetriever, compressor_settings: BaseCompressorSetting
) -> ContextualCompressionRetriever:
    """
    Adds a compressor to the retriever.

    Parameters
    ----------
    retriever : VectorStoreRetriever
        Base retriever.
    compressor_settings : BaseCompressorSetting
        Compressor settings.

    Returns
    -------
    New retriever with compressing feature.
    """
    if compressor_settings.max_documents:
        compressor_settings.max_documents = compressor_settings.max_documents

    compressor = get_compressor_factory(settings=compressor_settings).get_compressor()

    return ContextualCompressionRetriever(
        base_retriever=retriever,
        base_compressor=compressor,
    )


def format_documents(documents: List[Document], used_metadata: List[str]) -> str:
    """
    Formats list of documents to string.

    Parameters
    ----------
    documents : tuple of documents
        Documents to format.
    used_metadata : list of metadata
        Metadata to add to the prompt.

    Returns
    -------
    String with formatted documents as list.
    """
    context = ""
    for i, doc in enumerate(documents, start=1):
        concatenated_metadata = ", ".join(f"{k}: {v}" for k, v in doc.metadata.items() if k in used_metadata)
        context += f"\n\t{i} [{concatenated_metadata}] - {doc.page_content}\n"
    return context


def prepare_prompt(custom_template: str = None) -> PromptTemplate:
    """
    Creates a prompt template.

    Parameters
    ----------
    custom_template : str, optional
        A custom template provided as string.

    Returns
    -------
    A prompt template.
    """
    if custom_template:
        template = custom_template
    else:
        template = """Réponds à la question en te basant uniquement sur le sources suivantes:
        
        {context}
        
        Question: {question}
        """
    return PromptTemplate.from_template(template)


def _create_chain(
    prompt: PromptTemplate,
    llm: BaseLanguageModel,
    retriever: VectorStoreRetriever,
    used_metadata: List[str],
    guardrail_settings: BaseGuardrailSetting = None,
) -> RunnableSerializable:
    """
    Creates a RAG chain for processing queries with document retrieval and LLM generation.

    This function assembles a chain of operations that:
    1. Retrieves relevant documents using a retriever.
    2. Formats the retrieved documents and combines them with the user query using the provided prompt.
    3. Uses a LLM to generate an answer based on the formatted documents and query.
    4. Optionally applies a guardrail to ensure safe and valid outputs.
    5. Returns the constructed chain for further execution.

    Parameters
    ----------
    prompt : PromptTemplate
        The prompt template used for generating the final input to the LLM, formatted with the documents and question.

    llm : BaseLanguageModel
        The language model to generate answers based on the provided documents and question.

    retriever : VectorStoreRetriever
        A retriever used to fetch relevant documents from the vector store based on the question.

    used_metadata : list of string
        Metadata automatically appended to the prompt when transmitting chunks to the LLM.

    guardrail_settings : BaseGuardrailSetting, optional
        Settings for the guardrail mechanism to filter or validate the LLM's output. If not provided, a default output parser
        is used.

    Returns
    -------
    RunnableSerializable
        A serializable runnable chain that performs the document retrieval, prompt formatting, LLM generation,
        and guardrail processing (if provided).
    """
    rag_chain_from_docs = (
        {
            "context": lambda x: format_documents(x["documents"], used_metadata),
            "question": itemgetter("question"),
        }
        | prompt
        | llm
    )

    if guardrail_settings:
        guardrail = get_guardrail_factory(settings=guardrail_settings).get_parser()
        rag_chain_from_docs |= guardrail
    else:
        rag_chain_from_docs |= StrOutputParser()

    rag_chain_with_source = RunnableParallel(
        {"documents": retriever, "question": RunnablePassthrough()}
    ) | RunnableParallel(
        {
            "answer": rag_chain_from_docs,
            "sources": itemgetter("documents"),
        }
    )

    return rag_chain_with_source


def check_guardrail_output(guardrail_output: dict) -> bool:
    """
    Checks the output of a guardrail for toxicity and raises an exception if toxicity is detected.

    Parameters
    ----------
    guardrail_output : dict
        The output from the guardrail, typically containing fields such as 'output_toxicity' and 'output_toxicity_reason'.

    Returns
    -------
    bool
        Returns True if no toxicity is detected in the LLM output. If toxicity is detected, an exception is raised.

    Raises
    ------
    HTTPException
        If toxicity is detected, an HTTPException with a status code 451 is raised, along with details on the toxicity reasons.
    """
    if guardrail_output["output_toxicity"]:
        raise HTTPException(
            status_code=451,
            detail=f"Toxicity detected in LLM output ({','.join(guardrail_output['output_toxicity_reason'])})",
        )
    return True


def get_handlers(langfuse_settings: LangfuseSetting) -> dict[str, CallbackHandler]:
    """
    Creates and returns a dictionary of callback handlers based on the provided Langfuse settings.

    Parameters
    ----------
    langfuse_settings : LangfuseSetting
        The settings required to configure Langfuse.

    Returns
    -------
    dict[str, CallbackHandler]
        A dictionary with handler names as keys and corresponding CallbackHandler instances as values.
        If Langfuse settings are provided, the dictionary will contain a Langfuse handler; otherwise, it will be empty.
    """
    handlers = {}

    if langfuse_settings:
        handlers["langfuse"] = LangfuseHandler(
            langfuse_settings.public_key,
            langfuse_settings.secret_key,
            langfuse_settings.host,
            langfuse_settings.user_id,
            langfuse_settings.session_id,
        ).get_handler()

    return handlers


def stream_rag_chain(
    query: requests.RagQuery,
) -> Iterator[responses.SearchResponse | responses.AnswerResponse]:
    """
    Streams the RAG chain for answering a query, yielding search results and answers iteratively.

    Parameters
    ----------
    query : requests.RagQuery
        The query object containing all the necessary parameters for executing the RAG chain.

    Yields
    ------
    responses.SearchResponse
        If the chunk contains source documents, this response is yielded with the documents and associated metadata.
    responses.AnswerResponse
        If the chunk contains an answer, this response is yielded with the answer content.
    """
    rag_chain = init_chain(query)
    handlers = get_handlers(query.langfuse_settings)

    for chunk in rag_chain.stream(query.question, config={"callbacks": list(handlers.values())}):
        if "sources" in chunk:
            documents = []
            for document in chunk["sources"]:
                image_b64 = None
                if {"bucket", "blob"}.issubset(document.metadata.keys()):
                    image_b64 = download_gcs_image(document.metadata["bucket"], document.metadata["blob"])

                documents.append(
                    {"page_content": document.page_content, "metadata": document.metadata, "image": image_b64}
                )

            yield responses.SearchResponse(
                trace_id=(handlers["langfuse"].get_trace_id() if "langfuse" in handlers else None), documents=documents
            )
        else:
            if query.guardrail_settings:
                check_guardrail_output(chunk["answer"])
                yield responses.AnswerResponse(answer=chunk["answer"]["content"])
            else:
                yield responses.AnswerResponse(answer=chunk["answer"])


def invoke_rag_chain(query: requests.RagQuery) -> responses.RagResponse:
    """
    Executes the RAG chain for answering a query.

    This function invokes a pre-configured RAG chain to process a query, retrieving relevant documents and generating
    an answer. The result includes both the answer and the sources (documents) used to generate the answer. If guardrail
    settings are provided, the output is validated for toxicity before returning the result.

    Parameters
    ----------
    query : requests.RagQuery
        The query object containing the necessary parameters for executing the RAG chain.

    Returns
    -------
    responses.RagResponse
        A response object containing the generated answer and the relevant documents (sources) used to generate
        the answer. If guardrail settings are provided, the response will be filtered for toxicity before returning.
    """
    rag_chain = init_chain(query)
    handlers = get_handlers(query.langfuse_settings)

    result: dict = rag_chain.invoke(query.question, config={"callbacks": list(handlers.values())})

    if query.guardrail_settings:
        check_guardrail_output(result["answer"])

    documents = []
    for document in result["sources"]:
        image_b64 = None
        if {"bucket", "blob"}.issubset(document.metadata.keys()):
            image_b64 = download_gcs_image(document.metadata["bucket"], document.metadata["blob"])

        documents.append({"page_content": document.page_content, "metadata": document.metadata, "image": image_b64})

    return responses.RagResponse(
        trace_id=(handlers["langfuse"].get_trace_id() if "langfuse" in handlers else None),
        documents=documents,
        answer=(result["answer"]["content"] if "content" in result["answer"] else result["answer"]),
    )


def init_chain(
    query: requests.RagQuery,
) -> RunnableSerializable:
    """
    Initializes the RAG chain for processing a query by configuring the necessary components, including the
    language model, vector store retriever, and prompt template.

    Parameters
    ----------
    query : requests.RagQuery
        The query object containing the settings and configurations for the RAG chain.

    Returns
    -------
    RunnableSerializable
        A configured RAG chain that can be invoked to process the query. The chain includes the retriever,
        language model, and guardrail (if provided), ready to be executed with the query.
    """
    llm_model = get_llm_factory(settings=query.llm_settings).get_model()
    vector_store = get_vector_db_factory(
        db_settings=query.db_settings, em_settings=query.em_settings
    ).get_vector_store()
    search_kwargs = get_base_search_kwargs(query)

    search_kwargs["index"] = query.db_settings.index
    logger.info(f"Running vector similarity search with search_kwargs={json.dumps(search_kwargs)}")
    retriever = vector_store.as_retriever(search_kwargs=search_kwargs)
    if query.compressor_settings:
        retriever = add_compressor(retriever, query.compressor_settings)

    prompt = prepare_prompt(query.prompt_template)

    rag_chain_with_source = _create_chain(prompt, llm_model, retriever, query.used_metadata, query.guardrail_settings)

    return rag_chain_with_source
