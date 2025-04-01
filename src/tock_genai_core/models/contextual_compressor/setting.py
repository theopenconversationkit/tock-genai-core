from pydantic import BaseModel, Field
from typing import Optional

from tock_genai_core.models.contextual_compressor.provider import (
    ContextualCompressorProvider,
)
from tock_genai_core.models.security.security_type import SecretKey
from tock_genai_core.models.security.kube_secret_key import KubernetesSecretKey


class BaseCompressorSetting(BaseModel):
    """
    Base class for compressor settings.

    This class serves as a base for defining configuration settings for different contextual
    compressor providers.
    """

    provider: ContextualCompressorProvider = Field(description="The contextual compressor provider.")
    endpoint: str = Field(description="Scoring model endpoint.")
    api_key: Optional[SecretKey] = Field(
        description="The API key used to authenticate requests to the provider API.",
        default=None,
        examples=[KubernetesSecretKey(secret_name="openai_credentials")],
    )
