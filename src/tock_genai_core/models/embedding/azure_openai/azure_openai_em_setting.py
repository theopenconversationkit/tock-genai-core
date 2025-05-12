# -*- coding: utf-8 -*-
"""
AzureOpenAIEMSetting

Configuration settings for the AzureOpenAI embedding model.
This class defines the configuration required for using the AzureOpenAI embedding model.

Authors:
    * Baptiste Le Goff: baptiste.le-goff@arkea.com
    * Killian Mahé: killian.mahe@partnre.com
    * Luigi Bokalli: luigi.bokalli@partnre.com
    * Noé Chabanon: noe.chabanon@partnre.com
"""
from typing import Literal

from pydantic import Field

from tock_genai_core.models.embedding.provider import EMProvider
from tock_genai_core.models.embedding.setting import BaseEMSetting


class AzureOpenAIEMSetting(BaseEMSetting):
    """
    Configuration settings for the AzureOpenAI embedding model.
    This class defines the configuration required for using the AzureOpenAI embedding model.

    Attributes
    ----------
    provider: Literal[EMProvider.AzureOpenAI]
        The Embedding Model provider (default: EMProvider.AzureOpenAI)
    api_base: str
        Base endpoint of AzureOpenAI API
    api_version: str
        AzureOpenAI API version
    deployment: str
        Deployment name
    """

    provider: Literal[EMProvider.AzureOpenAI] = Field(
        description="The Embedding Model provider.", default=EMProvider.AzureOpenAI
    )
    api_base: str = Field(description="Base endpoint of AzureOpenAI API.")
    api_version: str = Field(description="AzureOpenAI API version.", examples=["2023-05-15"])
    deployment: str = Field(description="Deployment name.")
