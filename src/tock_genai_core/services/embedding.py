import logging
from urllib.parse import urljoin
from typing import Union, List, Optional

import requests
from pydantic import BaseModel
from langchain.schema.embeddings import Embeddings

logger = logging.getLogger(__name__)


class InferenceRequest(BaseModel):
    """
    A model representing a request for inference, containing text and pooling settings.

    Attributes
    ----------
    text : Union[str, list]
        The text input for the inference. This can either be a single string or a list of strings.
    pooling : str
        The pooling method to be applied during inference. This defines how the embeddings or features will be aggregated.
    """

    text: Union[str, list]
    pooling: str


class BloomzEmbeddings(BaseModel, Embeddings):
    """
    A model representing Bloomz embeddings, used for embedding documents and queries.

    Attributes
    ----------
    pooling : str
        The pooling method to be applied during embedding. This determines how the embeddings will be aggregated.
    api_base : str
        The base URL for the Bloomz embedding API.

    Methods
    -------
    _api_url() -> str
        Returns the full URL for the embedding API endpoint.

    embed_documents(texts: List[str]) -> List[List[float]]
        Sends a request to the embedding API to obtain embeddings for a list of documents (texts).

    embed_query(text: str) -> List[float]
        Computes embeddings for a single query by calling `embed_documents` with the query text.
    """

    pooling: str
    api_base: str
    api_key: Optional[str] = None

    @property
    def _api_url(self) -> str:
        return urljoin(self.api_base, "/embed")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Get the embeddings for a list of texts."""
        headers = {}
        if self.api_key:
            headers["Authentication"] = f"Bearer {self.api_key}"

        response = requests.post(
            self._api_url,
            json=InferenceRequest(text=texts, pooling=self.pooling).model_dump(mode="json"),
            headers=headers,
        )
        if response.status_code != 200:
            logger.exception(
                "Embedding request didn't return expected status code %s on chunk %s.", response.content, texts
            )
        return response.json()["embedding"]

    def embed_query(self, text: str) -> List[float]:
        """Compute query embeddings using a HuggingFace transformer model."""
        return self.embed_documents([text])[0]
