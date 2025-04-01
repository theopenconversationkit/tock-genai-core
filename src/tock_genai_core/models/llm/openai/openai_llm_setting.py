from typing import Literal

from pydantic import Field

from tock_genai_core.models.llm.provider import LLMProvider
from tock_genai_core.models.llm.setting import BaseLLMSetting


class OpenAILLMSetting(BaseLLMSetting):
    """
    Configuration settings for OpenAI LLM integration.
    This class defines the configuration required to connect to the OpenAI API
    """

    provider: Literal[LLMProvider.OpenAI] = Field(description="The Large Language Model provider.")
    api_base: str = Field(description="Base endpoint of OpenAI API.")
    api_version: str = Field(description="OpenAI API version.", examples=["2023-05-15"])
    deployment: str = Field(description="Deployment name.")
