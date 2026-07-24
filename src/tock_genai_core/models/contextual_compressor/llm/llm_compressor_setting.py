from typing import Literal, Optional

from pydantic import Field

from tock_genai_core.models.contextual_compressor.provider import (
    ContextualCompressorProvider,
)
from tock_genai_core.models.contextual_compressor.setting import BaseCompressorSetting
from tock_genai_core.models.llm.types import LLMSetting


class LLMCompressorSetting(BaseCompressorSetting):
    """
    Configuration settings for an LLM used as a reranker.

    Attributes
    ----------
    provider: Literal[ContextualCompressorProvider.LLM]
        The contextual compressor provider (default: ContextualCompressorProvider.LLM)
    provider_settings: LLMSetting
        The settings of the LLM chosen.
    min_score: float
        Minimum score to have to keep the document.
    max_documents: Optional[int]
        Maximum number of documents to return to avoid exceeding max tokens for text generation (default: 50)
    """

    provider: Literal[ContextualCompressorProvider.LLM] = Field(description="The contextual compressor provider.")
    provider_settings: LLMSetting = Field(description="The settings of the compressor provider.")
    min_score: float = Field(description="Minimum retailment score.")
    max_documents: Optional[int] = Field(
        description="Maximum number of documents to return to avoid exceeding max tokens for text generation.",
        default=50,
    )
    prompt: str = Field(
        description="Prompt",
        default="""Rate the relevance of this document to the query : 

                    Query: {query}

                    Document: {document}

                    Rate from 0-10 where:
                    - 0: Completely irrelevant
                    - 5: Partially relevant
                    - 10: Highly relevant and answers the query

                    ONLY return a number between 0 and 10 for the output.""",
    )
