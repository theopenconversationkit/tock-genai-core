from langchain_core.vectorstores import VectorStore
from langchain_community.vectorstores.opensearch_vector_search import OpenSearchVectorSearch

from tock_genai_core.models.database import OpenSearchSetting
from tock_genai_core.models.embedding import EMSetting
from tock_genai_core.services.langchain.factory.factories import VectorDBFactory
from tock_genai_core.services.langchain.factory.em_factory import get_em_factory
from tock_genai_core.services.security.security_service import fetch_secret_key_value


class OpenSearchFactory(VectorDBFactory):
    """
    Factory class for creating OpenSearch vector stores.
    This class is responsible for instantiating an `OpenSearchVectorSearch` object, using the configuration
    settings defined in the `OpenSearchSetting` and `EMSetting` classes.

    Attributes
    ----------
    db_settings : OpenSearchSetting
        The settings used to configure the OpenSearch connection.

    em_settings : EMSetting
        The settings used to configure the embedding model for the OpenSearch vector store.
    """

    db_settings: OpenSearchSetting
    em_settings: EMSetting

    def get_vector_store(self) -> VectorStore:
        """
        Returns an OpenSearch vector store instance configured with the provided settings.
        """
        return OpenSearchVectorSearch(
            index_name=self.db_settings.index,
            opensearch_url=self.db_settings.db_url,
            http_auth=(
                fetch_secret_key_value(self.db_settings.username),
                fetch_secret_key_value(self.db_settings.password),
            ),
            use_ssl=self.db_settings.use_ssl,
            verify_certs=self.db_settings.verify_certs,
            embedding_function=get_em_factory(settings=self.em_settings).get_model(),
            ssl_assert_hostname=False,
            ssl_show_warn=False,
        )
