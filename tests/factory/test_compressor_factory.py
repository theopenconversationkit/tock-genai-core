import pytest

from tock_genai_core.models.contextual_compressor import (
    ContextualCompressorProvider,
    BloomZCompressorSetting,
    LLMCompressorSetting,
)

# from tock_genai_core.services.compressor import LLMRerank
from tock_genai_core.services.langchain.factory import get_compressor_factory
from tock_genai_core.services.langchain.factory.contextual_compressor import (
    BloomzCompressorFactory,
    LLMCompressorFactory,
)
from tock_genai_core.models.llm import (
    LLMProvider,
    AzureOpenAILLMSetting,
)

from unittest import mock
from unittest.mock import patch, MagicMock
from langchain_core.documents import Document


@pytest.mark.parametrize(
    "settings, expected_output",
    [
        (
            BloomZCompressorSetting(
                provider=ContextualCompressorProvider.BloomZ, endpoint="http://bloomz", api_key=None, min_score=0.5
            ),
            BloomzCompressorFactory,
        ),
        (
            LLMCompressorSetting(
                provider=ContextualCompressorProvider.LLM,
                endpoint="http://bloomz",
                provider_settings=AzureOpenAILLMSetting(
                    provider=LLMProvider.AzureOpenAI,
                    model="model",
                    temperature=0.5,
                    api_base="http://api.com",
                    api_version="1.0.0",
                    deployment="deployment",
                ),
                min_score=0.5,
                max_documents=3,
            ),
            LLMCompressorFactory,
        ),
    ],
)
def test_get_compressor_factory(settings, expected_output):
    """Test for get_compressor_factory function"""
    factory = get_compressor_factory(settings)

    assert expected_output == type(factory)
