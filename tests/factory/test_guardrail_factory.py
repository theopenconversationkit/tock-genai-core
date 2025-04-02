import pytest

from tock_genai_core import (
    get_guardrail_factory,
    GuardrailProvider,
    BloomzGuardrailFactory,
    BloomZGuardrailSetting
)

@pytest.mark.parametrize("settings, expected_output", [
    (BloomZGuardrailSetting(provider= GuardrailProvider.BloomZ, api_base="http://api.com"), 
    BloomzGuardrailFactory)
])
def test_get_guardrail_factory(settings, expected_output):
    
    factory = get_guardrail_factory(settings)
    
    assert expected_output == type(factory)