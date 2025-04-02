import pytest

from tock_genai_core import (
    get_em_factory,
    EMProvider,
    BloomzFactory,
    OpenAIEMFactory,
    VLLMEMFactory,
    BloomZEMSetting,
    OpenAIEMSetting,
    VLLMEMSetting
)


@pytest.mark.parametrize("settings,  expected_output", [
    (BloomZEMSetting(provider= EMProvider.BloomZ, api_base="http://api.com"), 
     BloomzFactory),
    (OpenAIEMSetting(provider=EMProvider.OpenAI, api_base="http://api.com", api_version="1.0.0", deployment="deployment"), 
     OpenAIEMFactory),
    (VLLMEMSetting(provider=EMProvider.Vllm, api_base="http://api.com", model="model"), 
     VLLMEMFactory)
])
def test_get_em_factory(settings, expected_output):
    
    factory = get_em_factory(settings)
    
    assert expected_output == type(factory)
