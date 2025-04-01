from typing import Annotated, Union

from pydantic import Field

from tock_genai_core.models.embedding.bloomz.bloomz_em_setting import BloomZEMSetting
from tock_genai_core.models.embedding.openai.openai_em_setting import OpenAIEMSetting
from tock_genai_core.models.embedding.vllm.vllm_em_setting import VLLMEMSetting

# EMSetting is a type annotation that defines a union of possible embedding settings.
# The settings are determined by the value of the "provider" field, which acts as a discriminator.
EMSetting = Annotated[Union[BloomZEMSetting, OpenAIEMSetting, VLLMEMSetting], Field(discriminator="provider")]
