from langchain_postgres.vectorstores import PGVector

from tock_genai_core.models.database import PGVectorSetting
from tock_genai_core.models.embedding import EMSetting
from tock_genai_core.services.langchain.factory.factories import VectorDBFactory
from tock_genai_core.services.langchain.factory.em_factory import get_em_factory
from tock_genai_core.services.security.security_service import fetch_secret_key_value


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
        Returns a PGVector vector store instance configured with the provided settings.
        """
        return PGVector(
            collection_name=self.db_settings.index,
            distance_strategy=self.em_settings.space_type,
            use_jsonb=True,
            connection=self._get_connection_string(),
            embeddings=get_em_factory(settings=self.em_settings).get_model(),
            collection_metadata={"namespace": self.db_settings.namespace},
        )

    def _get_connection_string(self) -> str:
        """
        Constructs the PostgreSQL connection string using the provided database settings.

        Returns
        -------
        str
            The PostgreSQL connection string.
        """
        return (
            f"postgresql+psycopg://{fetch_secret_key_value(self.db_settings.username)}:{fetch_secret_key_value(self.db_settings.password)}"
            f"@{self.db_settings.db_url}/{self.db_settings.db_name}?sslmode={self.db_settings.sslmode}"
        )
