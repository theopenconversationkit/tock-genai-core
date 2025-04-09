from tock_genai_core.models.security.raw_secret_key import RawSecretKey
from tock_genai_core.services.security import fetch_secret_key_value


def test_raw_secrets__should_succeed():
    secret_value = "a1b2c3d4"
    secret = RawSecretKey(type="Raw", value=secret_value)
    assert fetch_secret_key_value(secret) == secret_value
