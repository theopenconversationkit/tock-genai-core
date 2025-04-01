from tock_genai_core.models.database import DBSetting
from tock_genai_core.models.embedding import BaseEMSetting
from tock_genai_core.models.database import VectorDBProvider
from tock_genai_core.services.langchain.factory.factories import VectorDBFactory, RelationalDBFactory
from tock_genai_core.services.langchain.factory.database import OpenSearchFactory, PGVectorFactory
from tock_genai_core.models.database.provider import RelationalDBProvider
from tock_genai_core.services.langchain.factory.database.postgres_factory import PostgresFactory


def get_vector_db_factory(db_settings: DBSetting, em_settings: BaseEMSetting) -> VectorDBFactory:
    """Creates a vector store factory based on the application name and embeddings settings provided.

    Parameters
    ----------
    db_settings : DBSetting
        Database configuration.
    em_settings : BaseEMSetting
        Embedding settings.

    Returns
    -------
    VectorDBFactory
    """
    if db_settings.provider == VectorDBProvider.OpenSearch:
        return OpenSearchFactory(
            db_settings=db_settings,
            em_settings=em_settings,
        )
    elif db_settings.provider == VectorDBProvider.PGVector:
        return PGVectorFactory(
            db_settings=db_settings,
            em_settings=em_settings,
        )


def get_relational_db_factory(db_settings: DBSetting) -> RelationalDBFactory:
    """Creates a relational database factory based on the database provider specified.

    Parameters
    ----------
    db_settings : DBSetting
        The configuration settings for the relational database provider, such as PostgreSQL.

    Returns
    -------
    RelationalDBFactory
        A factory for managing the specified relational database.
    """
    if db_settings.provider == RelationalDBProvider.PostgreSQL:
        return PostgresFactory(db_settings=db_settings)
