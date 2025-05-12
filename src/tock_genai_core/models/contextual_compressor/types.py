from typing import Annotated, Union

from pydantic import Field

from tock_genai_core.models.contextual_compressor.bloomz.bloomz_compressor_setting import (
    BloomZCompressorSetting,
)

# CompressorSetting is a type annotation that defines a union of possible compressor settings.
# The settings are determined by the value of the "provider" field, which acts as a discriminator.
CompressorSetting = Annotated[Union[BloomZCompressorSetting], Field(discriminator="provider")]
