import re
import logging
from urllib.parse import urljoin
from typing import Sequence, Optional

import requests
from langchain_core.documents import Document
from langchain.callbacks.manager import Callbacks
from langchain.retrievers.document_compressors.base import BaseDocumentCompressor
from tock_genai_core.services.langchain.factory.llm_factory import get_llm_factory
from tock_genai_core.models.contextual_compressor.provider import (
    ContextualCompressorProvider,
)
from langchain_core.prompts import ChatPromptTemplate
from tock_genai_core.models.llm.types import LLMSetting

logger = logging.getLogger(__name__)

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


class BloomzRerank(BaseDocumentCompressor):
    """Document compressor that uses `Bloomz reranking endpoint`."""

    min_score: float = 0.5
    """Minimum score to use for reranking."""
    endpoint: str
    """Model to use for reranking."""
    max_documents: int = 50
    """Maximum number of documents to return to avoid exceeding max tokens for text generation."""
    label: str = "entailment"
    """Label to use for reranking."""
    api_key: Optional[str] = None
    """The model API key."""

    def compress_documents(
        self,
        documents: Sequence[Document],
        query: str,
        callbacks: Optional[Callbacks] = None,
    ) -> Sequence[Document]:
        """
        Compress documents.

        Args:
            documents: A sequence of documents to compress.
            query: The query to use for compressing the documents.
            callbacks: Callbacks to run during the compression process.

        Returns:
            A sequence of compressed documents.
        """

        if len(documents) == 0:  # to avoid empty api call
            return []

        headers = {}
        if self.api_key:
            headers["Authentication"] = f"Bearer {self.api_key}"

        response = requests.post(
            urljoin(self.endpoint, "/score"),
            json={"contexts": [{"query": query, "context": document.page_content} for document in documents]},
            headers=headers,
        )

        if response.status_code != 200:
            logger.error("%s %s - %s", response.status_code, response.reason, response.text)
            raise RuntimeError("The scoring server didn't respond has expected.")

        final_results = []
        for i, doc_results in enumerate(response.json()["response"]):
            doc_entailment = list(filter(lambda cls: cls["label"] == self.label, doc_results))[0]
            if doc_entailment["score"] >= self.min_score:
                documents[i].metadata["retriever_score"] = doc_entailment["score"]
                final_results.append(documents[i])

        return sorted(final_results, key=lambda d: d.metadata["retriever_score"], reverse=True)[: self.max_documents]


class LLMRerank(BaseDocumentCompressor):
    """Document compressor that uses an llm to rerank documents"""

    """Provider of the contextualCompressor."""
    provider: ContextualCompressorProvider
    """Provider settings of the llm"""
    provider_settings: LLMSetting
    """Minimum score to obtain to keep a document"""
    min_score: float = 0.5
    """Maximum number of documents to returns"""
    max_documents: int = 50
    """Prompt"""
    prompt: str

    def compress_documents(
        self,
        documents: Sequence[Document],
        query: str,
        callbacks: Optional[Callbacks] = None,
    ) -> Sequence[Document]:
        """
        Compress documents.

        Args:
            documents: A sequence of documents to compress.
            query: The query to use for compressing the documents.
            callbacks: Callbacks to run during the compression process.

        Returns:
            A sequence of compressed documents.
        """

        # to avoid empty api call
        if len(documents) == 0:
            return []

        # compute the score of each document relative to the query
        documents_score = []
        for document in documents:
            try:
                score = self.get_reranking_score(query, document, settings=self.provider_settings)
                if score >= self.min_score:
                    document.metadata["retriever_score"] = score
                    documents_score.append(document)
            except Exception as e:
                logger.error("Error during scoring: %s", e)
                continue

        # sort the documents to keep a certain amount of documents (max_documents) with the maximum scores
        result = sorted(documents_score, key=lambda d: d.metadata["retriever_score"], reverse=True)[
            : self.max_documents
        ]

        # if no documents where found all document are return to make rage pipeline continue
        if not result:
            logger.warning("No relevant documents was found during reranking step")
            return documents  # fallback

        return result

    def build_reranking_prompt(self, query, document):
        """
        Build the reranking prompt.

        Args:
            query: The query to use for compressing the documents.
            document: Document to evaluate.

        Returns:
            A prompt
        """
        result = self.prompt.format(
            query=query,
            document=document.page_content,
        )

        return result

    def get_reranking_score(self, query, document, settings):
        """
        Score the document

        Args:
            query: The query to use for compressing the documents.
            document: Document to evaluate.
            settings: Settings of the llm

        Returns:
            A score
        """

        try:

            # llm model
            llm = get_llm_factory(settings=settings).get_model()

            # prompt
            prompt_str = self.build_reranking_prompt(query, document)
            prompt = ChatPromptTemplate.from_template(prompt_str)

            # chain
            chain = prompt | llm

            # score
            result = chain.invoke(
                input={
                    "query": query,
                    "document": document.page_content,
                }
            )
            # Chat models return a message object (`.content`), while completion-style LLMs
            # (e.g. VllmSetting/Qwen, backed by a `BaseLLM` such as `VLLMOpenAI`) return a plain
            # string directly - handle both instead of assuming a chat model.
            text = result.content if hasattr(result, "content") else result

            # Completion-style models without a chat template (e.g. Qwen via raw /v1/completions)
            # tend to ramble around the requested number instead of returning it alone, so extract
            # the first number found rather than parsing the whole output as a float.
            match = re.search(r"-?\d+(?:\.\d+)?", text)
            if not match:
                raise ValueError(f"No numeric score found in LLM output: {text!r}")

            return float(match.group())
        except Exception as e:
            raise RuntimeError(f"The scoring method didn't respond as expected : {e}")
