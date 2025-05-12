# -*- coding: utf-8 -*-
"""
BaseEMSetting

Base configuration settings for embedding models. This class defines the common settings used for
configuring embedding models from different providers.

Authors:
    * Baptiste Le Goff: baptiste.le-goff@arkea.com
    * Killian Mahé: killian.mahe@partnre.com
    * Luigi Bokalli: luigi.bokalli@partnre.com
    * Noé Chabanon: noe.chabanon@partnre.com
"""
from typing import Optional

from pydantic import BaseModel, Field

from tock_genai_core.models.embedding.provider import EMProvider
from tock_genai_core.models.security.security_type import SecretKey
from tock_genai_core.models.security.kube_secret_key import KubernetesSecretKey


class BaseEMSetting(BaseModel):
    """
    Base configuration settings for embedding models. This class defines the common settings used for
    configuring embedding models from different providers.

    Attributes
    ----------

    provider: EMProvider
        The Embedding Model provider
    model: Optional[str]
        Model name (default: None)
    api_key: Optional[SecretKey]
        The API key used to authenticate requests to the provider API (default: None)
    api_base: str
        The base url of the provider API
    pooling: Optional[str]
        Pooling method (default: None)
    space_type: Optional[str]
        The space type used to search vector (eg. `l2` for Bloomz, `cosin` for Ada) (default: l2)
    """

    provider: EMProvider = Field(description="The Embedding Model provider.")
    model: Optional[str] = Field(description="Model name.", default=None)
    api_key: Optional[SecretKey] = Field(
        description="The API key used to authenticate requests to the provider API.",
        default=None,
        examples=[KubernetesSecretKey(secret_name="openai_credentials")],
    )
    api_base: str = Field(description="The base url of the provider API.")
    pooling: Optional[str] = Field(description="Pooling method.", default=None, examples=["first", "mean", "last"])
    space_type: Optional[str] = Field(
        description="The space type used to search vector (eg. `l2` for Bloomz, `cosin` for Ada)",
        default="l2",
    )
