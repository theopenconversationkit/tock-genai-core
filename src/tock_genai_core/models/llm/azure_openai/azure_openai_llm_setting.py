# -*- coding: utf-8 -*-
"""
AzureOpenAILLMSetting

Configuration settings for AzureOpenAI LLM integration.
This class defines the configuration required to connect to the AzureOpenAI API

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


class AzureOpenAILLMSetting(BaseLLMSetting):
    """
    Configuration settings for AzureOpenAI LLM integration.
    This class defines the configuration required to connect to the AzureOpenAI API.

    Attributes
    ----------

    provider: Literal[LLMProvider.AzureOpenAI]
        The Large Language Model provider (default: LLMProvider.AzureOpenAI)
    api_base: str
        Base endpoint of AzureOpenAI API
    api_version: str
        AzureOpenAI API version
    deployment: str
        Deployment name
    """

    provider: Literal[LLMProvider.AzureOpenAI] = Field(
        description="The Large Language Model provider.", default=LLMProvider.AzureOpenAI
    )
    api_base: str = Field(description="Base endpoint of AzureOpenAI API.")
    api_version: str = Field(description="AzureOpenAI API version.", examples=["2023-05-15"])
    deployment: str = Field(description="Deployment name.")
