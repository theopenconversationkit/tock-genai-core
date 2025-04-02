import pytest

from tock_genai_core import (
    OpenSearchFactory, 
    PGVectorFactory, 
    OpenSearchSetting,
    PGVectorSetting,
    BloomZEMSetting, 
    EMProvider,
    VectorDBProvider,
    get_vector_db_factory
)


@pytest.mark.parametrize("db_settings,  expected_output", [
    (OpenSearchSetting(provider= VectorDBProvider.OpenSearch, db_url="http://localhost", use_ssl=False, verify_certs=False), 
     OpenSearchFactory),
    (PGVectorSetting(provider=VectorDBProvider.PGVector, db_url="http://localhost", namespace="namespace"), 
     PGVectorFactory)
])
def test_get_vector_db_factory(db_settings, expected_output):
    
    em_settings = BloomZEMSetting(provider=EMProvider.BloomZ, api_base="http://bloomz", pooling="")
    
    factory = get_vector_db_factory(db_settings, em_settings)
    
    assert expected_output == type(factory)


