from typing import Literal

from pydantic import Field

from tock_genai_core.models.guardrail.provider import GuardrailProvider
from tock_genai_core.models.guardrail.setting import BaseGuardrailSetting


class BloomZGuardrailSetting(BaseGuardrailSetting):
    """
    Configuration settings for the BloomZ guardrail model.
    This class defines the configuration required for using the BloomZ guardrail model.
    """

    provider: Literal[GuardrailProvider.BloomZ] = Field(description="The guardrail model provider.")
