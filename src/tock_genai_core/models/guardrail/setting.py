# -*- coding: utf-8 -*-
"""
BaseGuardrailSetting

Base configuration settings for guardrail models. This class defines the common settings used for
configuring guardrail models from different providers.

Authors:
    * Baptiste Le Goff: baptiste.le-goff@arkea.com
    * Killian Mahé: killian.mahe@partnre.com
    * Luigi Bokalli: luigi.bokalli@partnre.com
    * Noé Chabanon: noe.chabanon@partnre.com
"""
from typing import Optional
from pydantic import BaseModel, Field

from tock_genai_core.models.guardrail.provider import GuardrailProvider
from tock_genai_core.models.security.security_type import SecretKey
from tock_genai_core.models.security.kube_secret_key import KubernetesSecretKey


class BaseGuardrailSetting(BaseModel):
    """
    Base configuration settings for guardrail models. This class defines the common settings used for
    configuring guardrail models from different providers.

    Attributes
    ----------

    provider: GuardrailProvider
        The guardrail provider
    api_base: str
        The API base URL
    max_score: Optional[float]
        The maximum acceptable toxicity score (default: 0.3)
    api_key: Optional[SecretKey]
        The API key used to authenticate requests to the provider API (default: None)
    """

    provider: GuardrailProvider = Field(description="The guardrail provider.")
    api_base: str = Field(description="The API base URL.")
    max_score: Optional[float] = Field(description="The maximum acceptable toxicity score.", default=0.3)
    api_key: Optional[SecretKey] = Field(
        description="The API key used to authenticate requests to the provider API.",
        default=None,
        examples=[KubernetesSecretKey(secret_name="openai_credentials")],
    )
