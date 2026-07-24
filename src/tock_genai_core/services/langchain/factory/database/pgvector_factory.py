from functools import lru_cache

from sqlalchemy import create_engine, Engine
from langchain_postgres.vectorstores import PGVector

from tock_genai_core.models.database import PGVectorSetting
from tock_genai_core.models.embedding import EMSetting
from tock_genai_core.services.langchain.factory.factories import VectorDBFactory
from tock_genai_core.services.langchain.factory.em_factory import get_em_factory
from tock_genai_core.services.security.security_service import fetch_secret_key_value


@lru_cache(maxsize=32)
def _get_engine(db_url: str, db_name: str, sslmode: str, username: str, password: str) -> Engine:
    """
    Builds a SQLAlchemy Engine for the given connection target, reusing it (via lru_cache) across calls
    instead of letting PGVector open a new connection pool on every instantiation.

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


class PGVectorFactory(VectorDBFactory):
    """
    Factory class for creating PGVector vector stores.
    This class is responsible for instantiating a `PGVector` object using the settings defined in the
    `PGVectorSetting` and `EMSetting` classes.

    Attributes
    ----------
    db_settings : PGVectorSetting
        The settings used to configure the PostgreSQL database connection.

    em_settings : EMSetting
        The settings used to configure the embedding model for the PGVector vector store.
    """

    db_settings: PGVectorSetting
    em_settings: EMSetting

    def get_vector_store(self) -> PGVector:
        """
        Returns a PGVector vector store instance configured with the provided settings, backed by a
        shared, pooled Engine instead of a fresh connection per call.

        Returns
        -------
        PGVector
            A PGVector vector store instance bound to `self.db_settings.index`/`self.db_settings.namespace`,
            using a cached SQLAlchemy Engine and the embedding model resolved from `self.em_settings`.
        """
        engine = _get_engine(
            self.db_settings.db_url,
            self.db_settings.db_name,
            self.db_settings.sslmode,
            fetch_secret_key_value(self.db_settings.username),
            fetch_secret_key_value(self.db_settings.password),
        )
        return PGVector(
            collection_name=self.db_settings.index,
            distance_strategy=self.em_settings.space_type,
            use_jsonb=True,
            connection=engine,
            embeddings=get_em_factory(settings=self.em_settings).get_model(),
            collection_metadata={"namespace": self.db_settings.namespace},
            # The "vector" extension is already created by the langchain_postgres Alembic migration;
            # skip PGVector's own per-instantiation CREATE EXTENSION check.
            create_extension=False,
        )
