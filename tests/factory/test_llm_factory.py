import pytest

from tock_genai_core.services.langchain.factory import get_llm_factory
from tock_genai_core.models.llm import (
    LLMProvider,
    AzureOpenAILLMSetting,
    HuggingFaceTextGenInferenceLLMSetting,
    VllmSetting,
)
from tock_genai_core.services.langchain.factory.llm import TGIFactory, VllmFactory, AzureOpenAILLMFactory


@pytest.mark.parametrize(
    "settings,  expected_output",
    [
        (
            HuggingFaceTextGenInferenceLLMSetting(
                provider=LLMProvider.TGI,
                model="model",
                temperature=0.5,
                repetition_penalty=1.0,
                max_new_tokens=256,
                api_base="http://api.com",
                streaming=False,
            ),
            TGIFactory,
        ),
        (
            AzureOpenAILLMSetting(
                provider=LLMProvider.AzureOpenAI,
                model="model",
                temperature=0.5,
                api_base="http://api.com",
                api_version="1.0.0",
                deployment="deployment",
            ),
            AzureOpenAILLMFactory,
        ),
        (
            VllmSetting(
                provider=LLMProvider.Vllm, model="model", temperature=0.5, api_base="http://api.com", max_new_tokens=256
            ),
            VllmFactory,
        ),
    ],
)
def test_get_llm_factory(settings, expected_output):

    factory = get_llm_factory(settings)

    assert expected_output == type(factory)
