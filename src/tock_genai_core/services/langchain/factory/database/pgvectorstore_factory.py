import re
import uuid
from datetime import datetime
from functools import lru_cache
from typing import Optional

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from langchain_postgres import PGEngine, PGVectorStore
from langchain_postgres.v2.engine import Column
from langchain_postgres.v2.indexes import DistanceStrategy

from tock_genai_core.models.database.pgvector.pgvectorstore_db_setting import PGVectorStoreSetting
from tock_genai_core.models.embedding import EMSetting
from tock_genai_core.services.langchain.factory.factories import VectorDBFactory
from tock_genai_core.services.langchain.factory.em_factory import get_em_factory
from tock_genai_core.services.security.security_service import fetch_secret_key_value

_IDENTIFIER_RE = re.compile(r"^[a-z0-9_]+$")
_FTS_LANGUAGE_RE = re.compile(r"^[a-z]+$")

# `Column.data_type`/`fts_column`'s language are interpolated raw into DDL by langchain_postgres
# (it does not validate them itself, see `PGEngine._ainit_vectorstore_table`), and both
# `PGVectorStoreSetting.common_metadata_columns` and `.fts_column`/`.fts_language` are ordinary
# fields on a settings object that (in orchestrator_x260 at least) is deserialized straight from
# the API request body — so they must be treated as untrusted input, not just as trusted
# deployment config, and validated before ever reaching a SQL string.
_ALLOWED_SQL_TYPES = frozenset(
    {"TEXT", "INTEGER", "BIGINT", "BOOLEAN", "DOUBLE PRECISION", "REAL", "TIMESTAMP", "DATE", "UUID", "JSON", "JSONB"}
)

_DISTANCE_STRATEGY_MAP = {
    "l2": DistanceStrategy.EUCLIDEAN,
    "cosine": DistanceStrategy.COSINE_DISTANCE,
    "inner": DistanceStrategy.INNER_PRODUCT,
}


def _validate_identifier(value: str) -> str:
    """
    Validates that a value is safe to interpolate directly into raw SQL as an identifier (table or
    column name).

    Parameters
    ----------
    value : str
        The identifier to validate.

    Returns
    -------
    str
        The same value, unchanged, if valid.

    Raises
    ------
    ValueError
        If `value` contains anything other than lowercase letters, digits, or underscores.
    """
    if not _IDENTIFIER_RE.fullmatch(value):
        raise ValueError(f"Invalid identifier: {value!r}. Expected only [a-z0-9_].")
    return value


def _validate_table_name(table_name: str) -> str:
    """
    Validates that a table name is safe to interpolate directly into raw SQL as an identifier.

    Parameters
    ----------
    table_name : str
        The table name to validate.

    Returns
    -------
    str
        The same table name, unchanged, if valid.

    Raises
    ------
    ValueError
        If `table_name` contains anything other than lowercase letters, digits, or underscores.
    """
    return _validate_identifier(table_name)


def _validate_data_type(data_type: str) -> str:
    """
    Validates that a column's SQL data type is one of a known-safe allowlist.

    Parameters
    ----------
    data_type : str
        The SQL data type to validate (e.g. "TEXT", "INTEGER").

    Returns
    -------
    str
        The same data type, unchanged, if valid.

    Raises
    ------
    ValueError
        If `data_type` is not one of `_ALLOWED_SQL_TYPES`.
    """
    if data_type.upper() not in _ALLOWED_SQL_TYPES:
        raise ValueError(f"Unsupported column data_type: {data_type!r}. Expected one of {sorted(_ALLOWED_SQL_TYPES)}.")
    return data_type


def _validate_fts_language(language: str) -> str:
    """
    Validates that a full-text-search language/configuration name is safe to interpolate directly
    into raw SQL (as the first argument of `to_tsvector`/`to_tsquery`).

    Parameters
    ----------
    language : str
        The text-search configuration name to validate (e.g. "english", "french").

    Returns
    -------
    str
        The same value, unchanged, if valid.

    Raises
    ------
    ValueError
        If `language` contains anything other than lowercase letters.
    """
    if not _FTS_LANGUAGE_RE.fullmatch(language):
        raise ValueError(f"Invalid fts_language: {language!r}. Expected only lowercase letters.")
    return language


def _map_distance_strategy(space_type: Optional[str]) -> DistanceStrategy:
    """
    Maps a free-form `EMSetting.space_type` string to a v2 `DistanceStrategy` enum member.

    Parameters
    ----------
    space_type : Optional[str]
        The space type string (e.g. "l2", "cosine", "inner").

    Returns
    -------
    DistanceStrategy
        The corresponding v2 distance strategy.

    Raises
    ------
    ValueError
        If `space_type` does not match any known strategy.
    """
    if space_type not in _DISTANCE_STRATEGY_MAP:
        raise ValueError(f"Unsupported space_type: {space_type!r}. Expected one of {sorted(_DISTANCE_STRATEGY_MAP)}.")
    return _DISTANCE_STRATEGY_MAP[space_type]


@lru_cache(maxsize=32)
def _get_sync_engine(db_url: str, db_name: str, sslmode: str, username: str, password: str) -> Engine:
    """
    Builds a plain (sync) SQLAlchemy Engine for the given connection target, reusing it (via
    lru_cache) across calls. Used to read/write the `vectorstore_collections`/
    `vectorstore_metadata_fields` registry tables, which are plain relational tables that don't
    need the async `PGEngine` bridge.

    Parameters
    ----------
    db_url : str
        Host (and optional port) of the PostgreSQL server.
    db_name : str
        Name of the database to connect to.
    sslmode : str
        SSL mode to use for the connection (e.g. "require", "disable").
    username : str
        Resolved database username (already fetched from the secret store).
    password : str
        Resolved database password (already fetched from the secret store).

    Returns
    -------
    Engine
        A SQLAlchemy Engine with connection pooling configured (`pool_pre_ping`, `pool_recycle`,
        connection timeout), shared across all calls with the same arguments.
    """
    database_url = f"postgresql+psycopg://{username}:{password}@{db_url}/{db_name}?sslmode={sslmode}"
    return create_engine(
        database_url,
        pool_pre_ping=True,
        pool_recycle=1800,
        connect_args={"connect_timeout": 5},
    )


@lru_cache(maxsize=32)
def _get_engine(db_url: str, db_name: str, sslmode: str, username: str, password: str) -> PGEngine:
    """
    Builds a `PGEngine` (async, with a background event-loop thread) for the given connection
    target, reusing it (via lru_cache) across calls instead of letting `PGVectorStore` open a new
    connection pool on every instantiation.

    Parameters
    ----------
    db_url : str
        Host (and optional port) of the PostgreSQL server.
    db_name : str
        Name of the database to connect to.
    sslmode : str
        SSL mode to use for the connection (e.g. "require", "disable").
    username : str
        Resolved database username (already fetched from the secret store).
    password : str
        Resolved database password (already fetched from the secret store).

    Returns
    -------
    PGEngine
        A `PGEngine` built via `from_connection_string`, so that its sync methods (`create_sync`,
        `init_vectorstore_table`, ...) are usable (they require the background loop that only
        `from_connection_string` sets up, not `from_engine`).
    """
    database_url = f"postgresql+psycopg://{username}:{password}@{db_url}/{db_name}?sslmode={sslmode}"
    return PGEngine.from_connection_string(database_url)


class PGVectorStoreFactory(VectorDBFactory):
    """
    Factory class for creating PGVectorStore vector stores.
    This class is responsible for instantiating a `PGVectorStore` object using the settings defined
    in the `PGVectorStoreSetting` and `EMSetting` classes, provisioning its backing physical table
    (one per (index, namespace) pair) on first use.

    This is an alternative to `PGVectorFactory` (which builds the older, single-shared-table
    `PGVector` v1 vector store): opt-in via `provider=VectorDBProvider.PGVectorStore`, it does not
    change behavior for existing `PGVectorFactory`/`VectorDBProvider.PGVector` consumers.

    Attributes
    ----------
    db_settings : PGVectorStoreSetting
        The settings used to configure the PostgreSQL database connection.

    em_settings : EMSetting
        The settings used to configure the embedding model for the PGVectorStore vector store.
    """

    db_settings: PGVectorStoreSetting
    em_settings: EMSetting

    def get_vector_store(self) -> PGVectorStore:
        """
        Returns a PGVectorStore vector store instance for `self.db_settings.index`/`namespace`,
        provisioning its backing table (and registering it) on first use.

        Returns
        -------
        PGVectorStore
            A PGVectorStore instance bound to the physical table registered for
            `(self.db_settings.index, self.db_settings.namespace)`, using a cached `PGEngine` and
            the embedding model resolved from `self.em_settings`. Rebuilt on every call (never
            cached itself) so that metadata fields declared after this collection was first
            created are picked up immediately.

        Raises
        ------
        RuntimeError
            If the collection already exists but its stored `vector_size` no longer matches the
            current embedding model's dimension.
        """
        sync_engine = _get_sync_engine(
            self.db_settings.db_url,
            self.db_settings.db_name,
            self.db_settings.sslmode,
            fetch_secret_key_value(self.db_settings.username),
            fetch_secret_key_value(self.db_settings.password),
        )
        engine = _get_engine(
            self.db_settings.db_url,
            self.db_settings.db_name,
            self.db_settings.sslmode,
            fetch_secret_key_value(self.db_settings.username),
            fetch_secret_key_value(self.db_settings.password),
        )
        embeddings = get_em_factory(settings=self.em_settings).get_model()

        # Queries below use raw SQL (`text(...)`) rather than an ORM model, unlike orchestrator's
        # own db_queries.py which maps these same `vectorstore_collections`/
        # `vectorstore_metadata_fields` tables with SQLAlchemy ORM classes. tock-genai-core is the
        # generic, reusable library and has no dependency on orchestrator_x260, so it can't import
        # orchestrator's ORM classes for these tables; defining a second, competing ORM `Base` here
        # for the exact same tables would reintroduce the import-shadowing bug already fixed
        # elsewhere in this migration (two independent `Base`/metadata registries silently
        # overriding each other). Raw SQL avoids that risk at the cost of losing ORM convenience.
        with Session(sync_engine) as session:
            declared_columns = self._get_declared_columns(session)
            row = session.execute(
                text(
                    "SELECT table_name, vector_size FROM vectorstore_collections "
                    "WHERE index = :index AND namespace = :namespace"
                ),
                {"index": self.db_settings.index, "namespace": self.db_settings.namespace},
            ).first()

            if row is None:
                table_name, vector_size = self._provision_table(session, engine, embeddings, declared_columns)
            else:
                table_name, vector_size = row.table_name, row.vector_size
                actual_size = len(embeddings.embed_query("dimension probe"))
                if actual_size != vector_size:
                    raise RuntimeError(
                        f"Embedding model dimension ({actual_size}) does not match the existing "
                        f"table's vector size ({vector_size}) for index '{self.db_settings.index}' "
                        f"in namespace '{self.db_settings.namespace}'."
                    )

        metadata_column_names = [column.name for column in self._common_columns() + declared_columns]

        return PGVectorStore.create_sync(
            engine,
            embeddings,
            table_name=_validate_table_name(table_name),
            metadata_columns=metadata_column_names,
            distance_strategy=_map_distance_strategy(self.em_settings.space_type),
        )

    def _get_declared_columns(self, session: Session) -> list[Column]:
        """
        Reads the custom metadata fields declared as filterable for this (index, namespace) pair.

        Parameters
        ----------
        session : Session
            An open session on the registry (sync) engine.

        Returns
        -------
        list[Column]
            One `Column` per declared field, in the type expected by `init_vectorstore_table`/
            `PGVectorStore.create_sync`.
        """
        rows = session.execute(
            text(
                "SELECT field_name, field_type FROM vectorstore_metadata_fields "
                "WHERE index = :index AND namespace = :namespace"
            ),
            {"index": self.db_settings.index, "namespace": self.db_settings.namespace},
        ).all()
        # Defense in depth: these rows are expected to already be validated by whatever wrote them
        # (the metadata-fields declaration endpoint), but re-validating on read costs little and
        # protects against a corrupted/tampered row reaching raw DDL/SQL below.
        return [Column(_validate_identifier(row.field_name), _validate_data_type(row.field_type)) for row in rows]

    def _common_columns(self) -> list[Column]:
        """
        Builds the caller-supplied common metadata columns for every collection's table.

        tock-genai-core has no opinion of its own on which metadata fields every collection
        should always have: that's application-specific (e.g. orchestrator_x260 derives its list
        from its own `EmbeddingCMetadata` model). Callers configure this via
        `PGVectorStoreSetting.common_metadata_columns`; if unset, no common columns are created
        beyond what `PGVectorStore`'s own defaults provide.

        Returns
        -------
        list[Column]
            One `Column` per caller-configured common metadata field.
        """
        return [
            Column(_validate_identifier(field.name), _validate_data_type(field.data_type))
            for field in self.db_settings.common_metadata_columns or []
        ]

    def _provision_table(
        self,
        session: Session,
        engine: PGEngine,
        embeddings,
        declared_columns: list[Column],
    ) -> tuple[str, int]:
        """
        Creates the physical table for a brand-new (index, namespace) pair, its full-text index,
        and its registry row.

        Parameters
        ----------
        session : Session
            An open session on the registry (sync) engine, used to insert the registry row.
        engine : PGEngine
            The engine to create the vectorstore table on.
        embeddings : Embeddings
            The embedding model, used to probe the vector dimension.
        declared_columns : list[Column]
            Any custom metadata fields already declared for this (index, namespace) before its
            first use.

        Returns
        -------
        tuple[str, int]
            The newly provisioned `table_name` and `vector_size`. If a concurrent request won a
            race to provision the same (index, namespace) first, the winner's `table_name`/
            `vector_size` are returned instead (this request's own table is left in place, unused).
        """
        vector_size = len(embeddings.embed_query("dimension probe"))
        table_name = _validate_table_name(f"vs_{uuid.uuid4().hex}")

        engine.init_vectorstore_table(
            table_name,
            vector_size,
            metadata_columns=self._common_columns() + declared_columns,
            metadata_json_column="langchain_metadata",
        )
        # Full-text index is entirely opt-in (`PGVectorStoreSetting.fts_column`): tock-genai-core
        # has no opinion on whether a consumer needs lexical/hybrid search at all, only
        # orchestrator_x260 (IAFMLOPS-1682) does today. Left unset, no index is created for other
        # consumers.
        if self.db_settings.fts_column:
            # table_name interpolation is safe here: it was just generated above
            # (f"vs_{uuid4().hex}") and validated against `^[a-z0-9_]+$`, never derived from
            # request-body input. SQL has no bind-parameter syntax for identifiers (table/column
            # names), only for values, so this is the one place a table name has to be interpolated
            # rather than passed as a query param. `fts_column`/`fts_language` are validated above
            # (via `PGVectorStoreSetting`'s pydantic validation is NOT enough on its own: they are
            # re-validated by `_validate_identifier`/`_validate_fts_language` right here since they
            # are ordinary request-body fields, not trusted config).
            fts_column = _validate_identifier(self.db_settings.fts_column)
            fts_language = _validate_fts_language(self.db_settings.fts_language)
            session.execute(
                text(
                    f'CREATE INDEX IF NOT EXISTS "{table_name}_fts" ON "{table_name}" '
                    f"USING gin (to_tsvector('{fts_language}', {fts_column}))"
                )
            )

        try:
            session.execute(
                text(
                    "INSERT INTO vectorstore_collections (id, index, namespace, table_name, vector_size, created_at) "
                    "VALUES (:id, :index, :namespace, :table_name, :vector_size, :created_at)"
                ),
                {
                    "id": str(uuid.uuid4()),
                    "index": self.db_settings.index,
                    "namespace": self.db_settings.namespace,
                    "table_name": table_name,
                    "vector_size": vector_size,
                    "created_at": datetime.now(),
                },
            )
            session.commit()
            return table_name, vector_size
        except IntegrityError:
            # A concurrent request provisioned this (index, namespace) first: defer to it. The
            # table just created above is left in place (unused, harmless) rather than dropped,
            # to keep this path simple; it carries no registry row so it is never resolved again.
            session.rollback()
            winner = session.execute(
                text(
                    "SELECT table_name, vector_size FROM vectorstore_collections "
                    "WHERE index = :index AND namespace = :namespace"
                ),
                {"index": self.db_settings.index, "namespace": self.db_settings.namespace},
            ).first()
            return winner.table_name, winner.vector_size
