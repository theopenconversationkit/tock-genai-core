import pytest

from tock_genai_core.models.contextual_compressor import (
    ContextualCompressorProvider,
    LLMCompressorSetting,
)

from tock_genai_core.services.langchain.factory import get_compressor_factory
from tock_genai_core.models.llm import (
    LLMProvider,
    AzureOpenAILLMSetting,
)

from unittest import mock
from unittest.mock import patch, MagicMock
from langchain_core.documents import Document


@pytest.mark.parametrize(
    "settings, expected_output,score",
    [
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
            3,
            8,
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
            6,
            0,
        ),
    ],
)
@patch("tock_genai_core.services.compressor.LLMRerank.get_reranking_score")
def test_llm_reranker_should_succeed(mock_score, settings, expected_output, score):

    query = "Who is Steve?"

    documents = [
        Document(page_content="Steve is my friend from home. " "We went to school together and he lives near me."),
        Document(page_content="Sally is my friend from school. " "She likes mathematics."),
        Document(page_content="Football is a popular sport played worldwide."),
        Document(page_content="Steve Jobs was the founder of Apple and a technology entrepreneur."),
        Document(page_content="The weather is sunny today in Paris."),
        Document(page_content="Steve is not here tomorrow."),
    ]

    mock_score.return_value = score

    reranker = get_compressor_factory(settings).get_compressor()

    result = reranker.compress_documents(documents=documents, query=query)

    mock_score.assert_called()
    assert expected_output == len(result)
