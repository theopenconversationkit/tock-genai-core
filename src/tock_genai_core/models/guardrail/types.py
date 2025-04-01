from typing import Annotated, Union

from pydantic import Field

from tock_genai_core.models.guardrail.bloomz.bloomz_guardrail_setting import (
    BloomZGuardrailSetting,
)

# GuardrailSetting is a type annotation that defines a union of possible guardrail settings.
# The settings are determined by the value of the "provider" field, which acts as a discriminator.
GuardrailSetting = Annotated[Union[BloomZGuardrailSetting], Field(discriminator="provider")]
