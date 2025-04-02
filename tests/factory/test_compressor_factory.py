import pytest

from tock_genai_core import (
    get_compressor_factory,
    BloomzCompressorFactory,
    ContextualCompressorProvider,
    BloomZCompressorSetting
)

@pytest.mark.parametrize("settings, expected_output", [
    (BloomZCompressorSetting(provider= ContextualCompressorProvider.BloomZ, endpoint="http://bloomz", api_key=None, min_score=0.5), 
    BloomzCompressorFactory)
])
def test_get_compressor_factory(settings, expected_output):
    
    factory = get_compressor_factory(settings)
    
    assert expected_output == type(factory)