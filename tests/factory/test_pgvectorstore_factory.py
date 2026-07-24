from unittest.mock import MagicMock, patch

import pytest

from tock_genai_core.models.database import PGVectorStoreSetting, VectorDBProvider
from tock_genai_core.models.embedding import BloomZEMSetting, EMProvider
from tock_genai_core.models.security.raw_secret_key import RawSecretKey
from tock_genai_core.services.langchain.factory.database.pgvectorstore_factory import (
    PGVectorStoreFactory,
    _get_engine,
    _get_sync_engine,
    _map_distance_strategy,
    _validate_data_type,
    _validate_fts_language,
    _validate_table_name,
)


@pytest.fixture(autouse=True)
def clear_engine_caches():
    """Ensures the lru_cache on `_get_engine`/`_get_sync_engine` doesn't leak state between tests."""
    _get_engine.cache_clear()
    _get_sync_engine.cache_clear()
    yield
    _get_engine.cache_clear()
    _get_sync_engine.cache_clear()


def _db_settings(db_name: str = "test-db", **kwargs) -> PGVectorStoreSetting:
    return PGVectorStoreSetting(
        provider=VectorDBProvider.PGVectorStore,
        index="index_b",
        db_url="127.0.0.1:5432",
        sslmode="disable",
        username=RawSecretKey(type="Raw", value="user"),
        password=RawSecretKey(type="Raw", value="pwd"),
        namespace="123",
        db_name=db_name,
        **kwargs,
    )


def _em_settings() -> BloomZEMSetting:
    return BloomZEMSetting(provider=EMProvider.BloomZ, api_base="http://bloomz", pooling="", space_type="l2")


def _mock_embeddings(dimension: int = 3) -> MagicMock:
    embeddings = MagicMock()
    embeddings.embed_query.return_value = [0.1] * dimension
    return embeddings


def _mock_session_returning(registry_row, declared_field_rows=()) -> MagicMock:
    """
    Builds a mock whose `Session(...).__enter__()` returns a session where the first `.execute(...)`
    (the declared-fields query) yields `declared_field_rows` and the second (the registry lookup)
    yields `registry_row`. Any further `.execute(...)` call (GIN index creation, registry INSERT,
    made only on the "provision a new table" path) returns a generic MagicMock.
    """
    session = MagicMock()
    declared_result = MagicMock()
    declared_result.all.return_value = list(declared_field_rows)
    registry_result = MagicMock()
    registry_result.first.return_value = registry_row

    def execute_side_effect(*args, **kwargs):
        if not hasattr(execute_side_effect, "calls"):
            execute_side_effect.calls = 0
        execute_side_effect.calls += 1
        if execute_side_effect.calls == 1:
            return declared_result
        if execute_side_effect.calls == 2:
            return registry_result
        return MagicMock()

    session.execute.side_effect = execute_side_effect
    session_cm = MagicMock()
    session_cm.__enter__.return_value = session
    return session_cm, session


@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory.Session")
@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory.PGVectorStore")
@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory.get_em_factory")
@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory._get_engine")
@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory._get_sync_engine")
def test_get_vector_store_provisions_new_table_when_registry_row_missing(
    mocked_get_sync_engine, mocked_get_engine, mocked_get_em_factory, mocked_pgvectorstore, mocked_session_cls
):
    mocked_engine = MagicMock()
    mocked_get_engine.return_value = mocked_engine
    embeddings = _mock_embeddings()
    mocked_get_em_factory.return_value.get_model.return_value = embeddings

    session_cm, session = _mock_session_returning(registry_row=None)
    mocked_session_cls.return_value = session_cm

    vector_store = PGVectorStoreFactory(db_settings=_db_settings(), em_settings=_em_settings()).get_vector_store()

    mocked_engine.init_vectorstore_table.assert_called_once()
    _, init_kwargs = mocked_engine.init_vectorstore_table.call_args
    assert init_kwargs["metadata_json_column"] == "langchain_metadata"
    # No common_metadata_columns configured by this settings instance -> no forced columns.
    assert init_kwargs["metadata_columns"] == []

    # One execute() for the declared-fields lookup, one for the registry lookup, one for the
    # registry INSERT (no GIN index this time: fts_column unset).
    assert session.execute.call_count == 3
    session.commit.assert_called_once()

    mocked_pgvectorstore.create_sync.assert_called_once()
    assert vector_store is mocked_pgvectorstore.create_sync.return_value


@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory.Session")
@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory.PGVectorStore")
@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory.get_em_factory")
@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory._get_engine")
@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory._get_sync_engine")
def test_get_vector_store_provisions_common_columns_and_fts_index_when_configured(
    mocked_get_sync_engine, mocked_get_engine, mocked_get_em_factory, mocked_pgvectorstore, mocked_session_cls
):
    mocked_engine = MagicMock()
    mocked_get_engine.return_value = mocked_engine
    embeddings = _mock_embeddings()
    mocked_get_em_factory.return_value.get_model.return_value = embeddings

    session_cm, session = _mock_session_returning(registry_row=None)
    mocked_session_cls.return_value = session_cm

    settings = _db_settings(
        common_metadata_columns=[{"name": "title", "data_type": "TEXT"}],
        fts_column="content",
        fts_language="french",
    )
    PGVectorStoreFactory(db_settings=settings, em_settings=_em_settings()).get_vector_store()

    _, init_kwargs = mocked_engine.init_vectorstore_table.call_args
    assert [c.name for c in init_kwargs["metadata_columns"]] == ["title"]

    # 1 (declared fields) + 1 (registry lookup) + 1 (GIN index) + 1 (registry INSERT) = 4.
    assert session.execute.call_count == 4
    fts_sql = str(session.execute.call_args_list[2].args[0])
    assert "french" in fts_sql
    assert "content" in fts_sql


@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory.Session")
@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory.PGVectorStore")
@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory.get_em_factory")
@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory._get_engine")
@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory._get_sync_engine")
def test_get_vector_store_reuses_existing_table_without_reprovisioning(
    mocked_get_sync_engine, mocked_get_engine, mocked_get_em_factory, mocked_pgvectorstore, mocked_session_cls
):
    mocked_engine = MagicMock()
    mocked_get_engine.return_value = mocked_engine
    embeddings = _mock_embeddings(dimension=3)
    mocked_get_em_factory.return_value.get_model.return_value = embeddings

    registry_row = MagicMock(table_name="vs_existing", vector_size=3)
    session_cm, session = _mock_session_returning(registry_row=registry_row)
    mocked_session_cls.return_value = session_cm

    vector_store = PGVectorStoreFactory(db_settings=_db_settings(), em_settings=_em_settings()).get_vector_store()

    mocked_engine.init_vectorstore_table.assert_not_called()
    mocked_pgvectorstore.create_sync.assert_called_once()
    _, create_kwargs = mocked_pgvectorstore.create_sync.call_args
    assert create_kwargs["table_name"] == "vs_existing"
    assert vector_store is mocked_pgvectorstore.create_sync.return_value


@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory.Session")
@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory.PGVectorStore")
@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory.get_em_factory")
@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory._get_engine")
@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory._get_sync_engine")
def test_get_vector_store_raises_on_vector_size_mismatch(
    mocked_get_sync_engine, mocked_get_engine, mocked_get_em_factory, mocked_pgvectorstore, mocked_session_cls
):
    embeddings = _mock_embeddings(dimension=5)
    mocked_get_em_factory.return_value.get_model.return_value = embeddings

    registry_row = MagicMock(table_name="vs_existing", vector_size=3)
    session_cm, _ = _mock_session_returning(registry_row=registry_row)
    mocked_session_cls.return_value = session_cm

    with pytest.raises(RuntimeError, match="does not match"):
        PGVectorStoreFactory(db_settings=_db_settings(), em_settings=_em_settings()).get_vector_store()


@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory.Session")
@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory.PGVectorStore")
@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory.get_em_factory")
@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory._get_engine")
@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory._get_sync_engine")
def test_get_vector_store_rebuilds_pgvectorstore_every_call(
    mocked_get_sync_engine, mocked_get_engine, mocked_get_em_factory, mocked_pgvectorstore, mocked_session_cls
):
    """`PGVectorStore` must never be cached itself, only the underlying engine, so that a metadata
    field declared after the first call is picked up on the very next call."""
    embeddings = _mock_embeddings(dimension=3)
    mocked_get_em_factory.return_value.get_model.return_value = embeddings

    registry_row = MagicMock(table_name="vs_existing", vector_size=3)

    def make_session_cm():
        session_cm, _ = _mock_session_returning(registry_row=registry_row)
        return session_cm

    mocked_session_cls.side_effect = [make_session_cm(), make_session_cm()]

    factory = PGVectorStoreFactory(db_settings=_db_settings(), em_settings=_em_settings())
    factory.get_vector_store()
    factory.get_vector_store()

    assert mocked_pgvectorstore.create_sync.call_count == 2


def test_map_distance_strategy_valid():
    from langchain_postgres.v2.indexes import DistanceStrategy

    assert _map_distance_strategy("l2") == DistanceStrategy.EUCLIDEAN
    assert _map_distance_strategy("cosine") == DistanceStrategy.COSINE_DISTANCE
    assert _map_distance_strategy("inner") == DistanceStrategy.INNER_PRODUCT


def test_map_distance_strategy_invalid_raises():
    with pytest.raises(ValueError, match="Unsupported space_type"):
        _map_distance_strategy("not-a-real-strategy")


def test_validate_table_name_accepts_safe_names():
    assert _validate_table_name("vs_abc123") == "vs_abc123"


@pytest.mark.parametrize("bad_name", ["Vs_ABC", "vs-abc", "vs abc", "vs;DROP TABLE", ""])
def test_validate_table_name_rejects_unsafe_names(bad_name):
    with pytest.raises(ValueError, match="Invalid identifier"):
        _validate_table_name(bad_name)


def test_validate_data_type_accepts_allowlisted_types():
    assert _validate_data_type("TEXT") == "TEXT"
    assert _validate_data_type("integer") == "integer"


@pytest.mark.parametrize("bad_type", ["TEXT; DROP TABLE users", "NOTATYPE", ""])
def test_validate_data_type_rejects_unsafe_types(bad_type):
    with pytest.raises(ValueError, match="Unsupported column data_type"):
        _validate_data_type(bad_type)


def test_validate_fts_language_accepts_safe_values():
    assert _validate_fts_language("english") == "english"
    assert _validate_fts_language("french") == "french"


@pytest.mark.parametrize("bad_language", ["english; DROP TABLE users", "FR", "fr2", ""])
def test_validate_fts_language_rejects_unsafe_values(bad_language):
    with pytest.raises(ValueError, match="Invalid fts_language"):
        _validate_fts_language(bad_language)


@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory.create_engine")
def test_get_sync_engine_creates_engine_with_pooling_options(mocked_create_engine):
    mocked_create_engine.return_value = MagicMock()

    _get_sync_engine("127.0.0.1:5432", "test-db", "disable", "user", "pwd")

    mocked_create_engine.assert_called_once()
    args, kwargs = mocked_create_engine.call_args
    assert kwargs["pool_pre_ping"] is True
    assert kwargs["pool_recycle"] == 1800
    assert kwargs["connect_args"] == {"connect_timeout": 5}
    assert args[0] == "postgresql+psycopg://user:pwd@127.0.0.1:5432/test-db?sslmode=disable"


@patch("tock_genai_core.services.langchain.factory.database.pgvectorstore_factory.create_engine")
def test_get_sync_engine_reuses_cached_engine_for_same_target(mocked_create_engine):
    mocked_create_engine.return_value = MagicMock()

    engine1 = _get_sync_engine("127.0.0.1:5432", "test-db", "disable", "user", "pwd")
    engine2 = _get_sync_engine("127.0.0.1:5432", "test-db", "disable", "user", "pwd")

    mocked_create_engine.assert_called_once()
    assert engine1 is engine2
