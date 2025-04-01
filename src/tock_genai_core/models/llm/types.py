from typing import Union, Annotated

from pydantic import Field

from tock_genai_core.models.llm.tgi.tgi_llm_setting import (
    HuggingFaceTextGenInferenceLLMSetting,
)
from tock_genai_core.models.llm.openai.openai_llm_setting import OpenAILLMSetting
from tock_genai_core.models.llm.vllm.vllm_setting import VllmSetting

# LLMSetting is a type annotation that defines a union of possible guardrail settings.
# The settings are determined by the value of the "provider" field, which acts as a discriminator.
LLMSetting = Annotated[
    Union[HuggingFaceTextGenInferenceLLMSetting, OpenAILLMSetting, VllmSetting],
    Field(discriminator="provider"),
]
