import logging
from urllib.parse import urljoin
from typing import Sequence, Optional

import requests
from langchain_core.documents import Document
from langchain.callbacks.manager import Callbacks
from langchain.retrievers.document_compressors.base import BaseDocumentCompressor


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
