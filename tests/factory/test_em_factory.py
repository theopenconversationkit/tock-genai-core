import pytest

from tock_genai_core.models.embedding import EMProvider
from tock_genai_core.services.langchain.factory import get_em_factory
from tock_genai_core.services.langchain.factory.embedding import BloomzFactory, AzureOpenAIEMFactory, VLLMEMFactory
from tock_genai_core.models.embedding import BloomZEMSetting, AzureOpenAIEMSetting, VLLMEMSetting


@pytest.mark.parametrize("settings,  expected_output", [
    (BloomZEMSetting(provider= EMProvider.BloomZ, api_base="http://api.com"), 
     BloomzFactory),
    (AzureOpenAIEMSetting(provider=EMProvider.AzureOpenAI, api_base="http://api.com", api_version="1.0.0", deployment="deployment"), 
     AzureOpenAIEMFactory),
    (VLLMEMSetting(provider=EMProvider.Vllm, api_base="http://api.com", model="model"), 
     VLLMEMFactory)
])
def test_get_em_factory(settings, expected_output):
    
    factory = get_em_factory(settings)
    
    assert expected_output == type(factory)
