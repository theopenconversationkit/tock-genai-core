from unittest.mock import MagicMock, patch

import pytest

from tock_genai_core.models.database import PGVectorSetting, VectorDBProvider
from tock_genai_core.models.embedding import BloomZEMSetting, EMProvider
from tock_genai_core.models.security.raw_secret_key import RawSecretKey
from tock_genai_core.services.langchain.factory.database.pgvector_factory import PGVectorFactory, _get_engine


@pytest.fixture(autouse=True)
def clear_engine_cache():
    """Ensures the lru_cache on `_get_engine` doesn't leak state between tests."""
    _get_engine.cache_clear()
    yield
    _get_engine.cache_clear()


def _db_settings(db_name: str = "test-db") -> PGVectorSetting:
    return PGVectorSetting(
        provider=VectorDBProvider.PGVector,
        index="index_b",
        db_url="127.0.0.1:5432",
        sslmode="disable",
        username=RawSecretKey(value="user", type="Raw"),
        password=RawSecretKey(value="pwd", type="Raw"),
        namespace="123",
        db_name=db_name,
    )


def _em_settings() -> BloomZEMSetting:
    return BloomZEMSetting(provider=EMProvider.BloomZ, api_base="http://bloomz", pooling="")


@patch("tock_genai_core.services.langchain.factory.database.pgvector_factory.PGVector")
@patch("tock_genai_core.services.langchain.factory.database.pgvector_factory.get_em_factory")
@patch("tock_genai_core.services.langchain.factory.database.pgvector_factory.create_engine")
def test_get_vector_store_uses_cached_engine_and_skips_extension_creation(
    mocked_create_engine, mocked_get_em_factory, mocked_pgvector
):
    """
    `get_vector_store` must pass a shared Engine (not a connection string) to `PGVector`, and disable
    its own `create_extension` step since the Alembic migration already creates the "vector" extension.
    """
    mocked_engine = MagicMock()
    mocked_create_engine.return_value = mocked_engine
    mocked_embeddings = MagicMock()
    mocked_get_em_factory.return_value.get_model.return_value = mocked_embeddings

    factory = PGVectorFactory(db_settings=_db_settings(), em_settings=_em_settings())
    vector_store = factory.get_vector_store()

    mocked_create_engine.assert_called_once()
    _, create_engine_kwargs = mocked_create_engine.call_args
    assert create_engine_kwargs["pool_pre_ping"] is True
    assert create_engine_kwargs["pool_recycle"] == 1800
    assert create_engine_kwargs["connect_args"] == {"connect_timeout": 5}

    mocked_pgvector.assert_called_once_with(
        collection_name="index_b",
        distance_strategy="l2",
        use_jsonb=True,
        connection=mocked_engine,
        embeddings=mocked_embeddings,
        collection_metadata={"namespace": "123"},
        create_extension=False,
    )
    assert vector_store is mocked_pgvector.return_value


@patch("tock_genai_core.services.langchain.factory.database.pgvector_factory.PGVector")
@patch("tock_genai_core.services.langchain.factory.database.pgvector_factory.get_em_factory")
@patch("tock_genai_core.services.langchain.factory.database.pgvector_factory.create_engine")
def test_get_vector_store_reuses_engine_across_calls_for_same_target(
    mocked_create_engine, mocked_get_em_factory, mocked_pgvector
):
    mocked_create_engine.return_value = MagicMock()
    mocked_get_em_factory.return_value.get_model.return_value = MagicMock()

    factory = PGVectorFactory(db_settings=_db_settings(), em_settings=_em_settings())
    factory.get_vector_store()
    factory.get_vector_store()

    mocked_create_engine.assert_called_once()


@patch("tock_genai_core.services.langchain.factory.database.pgvector_factory.PGVector")
@patch("tock_genai_core.services.langchain.factory.database.pgvector_factory.get_em_factory")
@patch("tock_genai_core.services.langchain.factory.database.pgvector_factory.create_engine")
def test_get_vector_store_creates_distinct_engine_for_different_target(
    mocked_create_engine, mocked_get_em_factory, mocked_pgvector
):
    mocked_create_engine.side_effect = [MagicMock(), MagicMock()]
    mocked_get_em_factory.return_value.get_model.return_value = MagicMock()

    PGVectorFactory(db_settings=_db_settings(db_name="db-one"), em_settings=_em_settings()).get_vector_store()
    PGVectorFactory(db_settings=_db_settings(db_name="db-two"), em_settings=_em_settings()).get_vector_store()

    assert mocked_create_engine.call_count == 2
