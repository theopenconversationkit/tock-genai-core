from typing import Literal

from pydantic import Field

from tock_genai_core.models.embedding.provider import EMProvider
from tock_genai_core.models.embedding.setting import BaseEMSetting


class OpenAIEMSetting(BaseEMSetting):
    """
    Configuration settings for the OpenAI embedding model.
    This class defines the configuration required for using the OpenAI embedding model.
    """

    provider: Literal[EMProvider.OpenAI] = Field(description="The Embedding Model provider.")
    api_base: str = Field(description="Base endpoint of OpenAI API.")
    api_version: str = Field(description="OpenAI API version.", examples=["2023-05-15"])
    deployment: str = Field(description="Deployment name.")
