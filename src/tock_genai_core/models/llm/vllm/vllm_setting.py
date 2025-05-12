# -*- coding: utf-8 -*-
"""
VllmSetting

Configuration settings for the VLLM (Qwen) LLM integration.
This class defines the configuration required to connect to the VLLM API.

Authors:
    * Baptiste Le Goff: baptiste.le-goff@arkea.com
    * Killian Mahé: killian.mahe@partnre.com
    * Luigi Bokalli: luigi.bokalli@partnre.com
    * Noé Chabanon: noe.chabanon@partnre.com
"""
from typing import Any, Dict, Literal, Optional

from pydantic import Field

from tock_genai_core.models.llm.provider import LLMProvider
from tock_genai_core.models.llm.setting import BaseLLMSetting


class VllmSetting(BaseLLMSetting):
    """
    Configuration settings for the VLLM (Qwen) LLM integration.

    This class defines the configuration required to connect to the VLLM API.

    Attributes
    ----------
    provider: Literal[LLMProvider.Vllm]
        The Large Language Model provider (default: LLMProvider.Vllm)
    api_base: str
        Base endpoint of Qwen/Vllm API
    max_new_tokens: int
        Maximum length of the llm response (default: 256)
    additional_model_kwargs: Optional[Dict[str, Any]]
        Additional arguments (default: {})
    """

    provider: Literal[LLMProvider.Vllm] = Field(
        description="The Large Language Model provider.", default=LLMProvider.Vllm
    )
    api_base: str = Field(description="Base endpoint of Qwen/Vllm API.")
    max_new_tokens: int = Field(description="Maximum length of the llm response.", default=256)
    additional_model_kwargs: Optional[Dict[str, Any]] = Field(description="Additional arguments.", default={})
