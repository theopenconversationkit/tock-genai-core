from typing import Annotated, Union

from pydantic import Field

from tock_genai_core.models.contextual_compressor.bloomz.bloomz_compressor_setting import (
    BloomZCompressorSetting,
)
from tock_genai_core.models.contextual_compressor.llm.llm_compressor_setting import (
    LLMCompressorSetting,
)

# CompressorSetting is a type annotation that defines a union of possible compressor settings.
# The settings are determined by the value of the "provider" field, which acts as a discriminator.
CompressorSetting = Annotated[
    Union[BloomZCompressorSetting, LLMCompressorSetting],
    Field(discriminator="provider"),
]
