from typing import Literal
from pydantic import Field

from tock_genai_core.models.embedding.provider import EMProvider
from tock_genai_core.models.embedding.setting import BaseEMSetting


class VLLMEMSetting(BaseEMSetting):
    provider: Literal[EMProvider.Vllm] = Field(description="The Embedding Model provider.")
    model: str = Field(description="Model name.")
