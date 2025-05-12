import pytest

from tock_genai_core.models.contextual_compressor import ContextualCompressorProvider, BloomZCompressorSetting
from tock_genai_core.services.langchain.factory import get_compressor_factory
from tock_genai_core.services.langchain.factory.contextual_compressor import BloomzCompressorFactory


@pytest.mark.parametrize(
    "settings, expected_output",
    [
        (
            BloomZCompressorSetting(
                provider=ContextualCompressorProvider.BloomZ, endpoint="http://bloomz", api_key=None, min_score=0.5
            ),
            BloomzCompressorFactory,
        )
    ],
)
def test_get_compressor_factory(settings, expected_output):
    """Test for get_compressor_factory function"""
    factory = get_compressor_factory(settings)

    assert expected_output == type(factory)
