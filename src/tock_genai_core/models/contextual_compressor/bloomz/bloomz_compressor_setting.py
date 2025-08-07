# -*- coding: utf-8 -*-
"""
BloomZCompressorSetting

Configuration settings for the BloomZ contextual compressor.
This class defines the parameters used to configure the BloomZ-based reranking compressor,
which selects the most relevant documents based on a minimum entailment score.

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
    Settings for configuring the BloomZ-based contextual compression.

    This configuration is used to control how documents are filtered and reranked
    using the BloomZ model, typically in retrieval-augmented generation (RAG) pipelines.

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
