from tock_genai_core.models.database import DBSetting
from tock_genai_core.models.embedding import BaseEMSetting
from tock_genai_core.models.database import VectorDBProvider
from tock_genai_core.services.langchain.factory.factories import VectorDBFactory
from tock_genai_core.services.langchain.factory.database import OpenSearchFactory, PGVectorFactory


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
    if db_settings.provider == VectorDBProvider.PGVector:
        return PGVectorFactory(
            db_settings=db_settings,
            em_settings=em_settings,
        )
