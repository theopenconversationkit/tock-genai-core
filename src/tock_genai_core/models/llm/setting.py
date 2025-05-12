# -*- coding: utf-8 -*-
"""
BaseLLMSetting

Base configuration settings for LLM API. This class defines the common settings used for
configuring LLM API from different providers.

Authors:
    * Baptiste Le Goff: baptiste.le-goff@arkea.com
    * Killian Mahé: killian.mahe@partnre.com
    * Luigi Bokalli: luigi.bokalli@partnre.com
    * Noé Chabanon: noe.chabanon@partnre.com
"""
from typing import Optional

from pydantic import BaseModel, Field

from tock_genai_core.models.llm.provider import LLMProvider
from tock_genai_core.models.security.security_type import RawSecretKey, SecretKey


class BaseLLMSetting(BaseModel):
    """
    Base configuration settings for LLM API. This class defines the common settings used for
    configuring LLM API from different providers.

    Attributes
    ----------

    provider: LLMProvider
        The Large Language Model provider
    model: Optional[str]
        Model name (default: None)
    api_key: Optional[SecretKey]
        The API key used to authenticate requests to the provider API (default: None)
    temperature: float
        The temperature that controls the randomness of the text generated (default: 0.5)

    """

    provider: LLMProvider = Field(description="The Large Language Model provider.")
    model: Optional[str] = Field(description="Model name.", default=None)
    api_key: Optional[SecretKey] = Field(
        description="The API key used to authenticate requests to the provider API.",
        default=None,
        examples=[RawSecretKey(value="145d-ff455g-e4r5gf")],
    )
    temperature: float = Field(
        description="The temperature that controls the randomness of the text generated.",
        examples=["0.1"],
        default=0.5,
        ge=0,
        le=2,
    )
