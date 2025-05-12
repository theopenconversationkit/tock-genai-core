# -*- coding: utf-8 -*-
"""
BloomZCompressorSetting

Configuration settings for OpenSearch vector database.
This class defines the configuration for connecting to an OpenSearch vector database.

Authors:
    * Baptiste Le Goff: baptiste.le-goff@arkea.com
    * Killian Mahé: killian.mahe@partnre.com
    * Luigi Bokalli: luigi.bokalli@partnre.com
    * Noé Chabanon: noe.chabanon@partnre.com
"""
from typing import Literal, Optional

from pydantic import Field

from tock_genai_core.models.contextual_compressor.provider import (
    ContextualCompressorProvider,
)
from tock_genai_core.models.contextual_compressor.setting import BaseCompressorSetting


class BloomZCompressorSetting(BaseCompressorSetting):
    """
    Configuration settings for OpenSearch vector database.
    This class defines the configuration for connecting to an OpenSearch vector database.

    Attributes
    ----------
    provider: Literal[ContextualCompressorProvider.BloomZ]
        The contextual compressor provider (default: ContextualCompressorProvider.BloomZ)
    min_score: float
        Minimum retailment score
    max_documents: Optional[int]
        Maximum number of documents to return to avoid exceeding max tokens for text generation (default: 50)
    label: Optional[str]
        Label to use for reranking (default: entailment)
    """

    provider: Literal[ContextualCompressorProvider.BloomZ] = Field(
        description="The contextual compressor provider.", default=ContextualCompressorProvider.BloomZ
    )
    min_score: float = Field(description="Minimum retailment score.")
    max_documents: Optional[int] = Field(
        description="Maximum number of documents to return to avoid exceeding max tokens for text generation.",
        default=50,
    )
    label: Optional[str] = Field(description="Label to use for reranking.", default="entailment")
