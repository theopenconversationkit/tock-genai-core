import pytest

from tock_genai_core.models.database import PGVectorSetting, VectorDBProvider
from tock_genai_core.models.embedding import BloomZEMSetting, EMProvider
from tock_genai_core.services.langchain.factory import get_vector_db_factory
from tock_genai_core.services.langchain.factory.database import PGVectorFactory


@pytest.mark.parametrize(
    "db_settings,  expected_output",
    [
        (
            PGVectorSetting(provider=VectorDBProvider.PGVector, db_url="http://localhost", namespace="namespace"),
            PGVectorFactory,
        ),
    ],
)
def test_get_vector_db_factory(db_settings, expected_output):
    """Test for get_vector_db_factory function"""

    em_settings = BloomZEMSetting(provider=EMProvider.BloomZ, api_base="http://bloomz", pooling="")

    factory = get_vector_db_factory(db_settings, em_settings)

    assert expected_output == type(factory)
