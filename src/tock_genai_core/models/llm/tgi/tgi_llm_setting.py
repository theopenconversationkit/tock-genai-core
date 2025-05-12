# -*- coding: utf-8 -*-
"""
HuggingFaceTextGenInferenceLLMSetting

Configuration settings for Hugging Face Text Generation Inference LLM integration.
This class defines the configuration required to connect to the Hugging Face Text Generation Inference API.

Authors:
    * Baptiste Le Goff: baptiste.le-goff@arkea.com
    * Killian Mahé: killian.mahe@partnre.com
    * Luigi Bokalli: luigi.bokalli@partnre.com
    * Noé Chabanon: noe.chabanon@partnre.com
"""
from typing import Literal

from pydantic import Field

from tock_genai_core.models.llm.provider import LLMProvider
from tock_genai_core.models.llm.setting import BaseLLMSetting


class HuggingFaceTextGenInferenceLLMSetting(BaseLLMSetting):
    """
    Configuration settings for Hugging Face Text Generation Inference LLM integration.
    This class defines the configuration required to connect to the Hugging Face Text Generation Inference API.

    Attributes
    ----------

    provider: Literal[LLMProvider.TGI]
        The Large Language Model provider (default: LLMProvider.TGI)
    repetition_penalty: float
        Penalty on model repetition (default: 1.0)
    max_new_tokens: int
        Maximum length of the llm response (default: 256)
    api_base: str
        TGI API base URL
    streaming: bool
        Enable streaming response (default: False)
    """

    provider: Literal[LLMProvider.TGI] = Field(
        description="The Large Language Model provider.", default=LLMProvider.TGI
    )
    repetition_penalty: float = Field(description="Penalty on model repetition.", default=1.0)
    max_new_tokens: int = Field(description="Maximum length of the llm response.", default=256)
    api_base: str = Field(description="TGI API base URL.")
    streaming: bool = Field(description="Enable streaming response.", default=False)
