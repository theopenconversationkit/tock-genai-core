import pytest

from tock_genai_core.services.langchain.factory import get_guardrail_factory
from tock_genai_core.services.langchain.factory.guardrail import BloomzGuardrailFactory
from tock_genai_core.models.guardrail import GuardrailProvider, BloomZGuardrailSetting


@pytest.mark.parametrize("settings, expected_output", [
    (BloomZGuardrailSetting(provider= GuardrailProvider.BloomZ, api_base="http://api.com"), 
    BloomzGuardrailFactory)
])
def test_get_guardrail_factory(settings, expected_output):
    
    factory = get_guardrail_factory(settings)
    
    assert expected_output == type(factory)