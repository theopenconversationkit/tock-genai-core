from unittest.mock import MagicMock, patch

import pytest

from tock_genai_core.models.security.raw_secret_key import RawSecretKey
from tock_genai_core.services.langfuse.handler import LangfuseHandler


PUBLIC_KEY = RawSecretKey(type="Raw", value="pk-lf-test")
SECRET_KEY = RawSecretKey(type="Raw", value="sk-lf-test")
HOST = "https://langfuse.example.com"


@pytest.fixture
def handler():
    return LangfuseHandler(public_key=PUBLIC_KEY, secret_key=SECRET_KEY, host=HOST)


def test_exists__with_valid_key(handler):
    assert handler.exists() is True


def test_exists__with_none_key():
    with patch("tock_genai_core.services.langfuse.handler.fetch_secret_key_value", return_value=None):
        h = LangfuseHandler(public_key=PUBLIC_KEY, secret_key=SECRET_KEY, host=HOST)
    assert h.exists() is False


@patch("tock_genai_core.services.langfuse.handler.Langfuse")
def test_get_client__initializes_with_correct_params(mock_langfuse, handler):
    handler.get_client()

    mock_langfuse.assert_called_once_with(
        public_key="pk-lf-test",
        secret_key="sk-lf-test",
        base_url=HOST,
    )


@patch("tock_genai_core.services.langfuse.handler.Langfuse")
def test_get_client__returns_cached_instance(mock_langfuse, handler):
    client1 = handler.get_client()
    client2 = handler.get_client()

    assert client1 is client2
    mock_langfuse.assert_called_once()


@patch("tock_genai_core.services.langfuse.handler.CallbackHandler")
@patch("tock_genai_core.services.langfuse.handler.Langfuse")
def test_get_handler__initializes_langfuse_then_returns_callback(mock_langfuse, mock_callback_handler, handler):
    result = handler.get_handler()

    mock_langfuse.assert_called_once_with(
        public_key="pk-lf-test",
        secret_key="sk-lf-test",
        base_url=HOST,
    )
    mock_callback_handler.assert_called_once_with()
    assert result is mock_callback_handler.return_value
