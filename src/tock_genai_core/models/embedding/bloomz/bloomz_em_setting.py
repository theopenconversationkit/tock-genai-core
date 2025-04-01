from typing import Literal

from pydantic import Field

from tock_genai_core.models.embedding.provider import EMProvider
from tock_genai_core.models.embedding.setting import BaseEMSetting


class BloomZEMSetting(BaseEMSetting):
    """
    Configuration settings for the BloomZ embedding model.
    This class defines the configuration required for using the BloomZ embedding model.
    """

    provider: Literal[EMProvider.BloomZ] = Field(description="The Embedding Model provider.", default=EMProvider.BloomZ)
