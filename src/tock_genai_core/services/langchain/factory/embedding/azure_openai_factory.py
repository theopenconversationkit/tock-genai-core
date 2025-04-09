from langchain.embeddings.base import Embeddings
from langchain_openai import AzureOpenAIEmbeddings

from tock_genai_core.models.embedding import AzureOpenAIEMSetting
from tock_genai_core.services.langchain.factory.factories import EMFactory
from tock_genai_core.services.security.security_service import fetch_secret_key_value


class AzureOpenAIEMFactory(EMFactory):
    """
    Factory class for creating AzureOpenAI Embedding model instances.
    This class is responsible for instantiating an `AzureOpenAIEmbeddings` object using the settings defined
    in the `AzureOpenAIEMSetting` class.

    Attributes
    ----------
    settings : AzureOpenAIEMSetting
        The settings used to configure the AzureOpenAIEmbeddings model.
    """

    settings: AzureOpenAIEMSetting

    def get_model(self) -> Embeddings:
        """
        Returns an AzureOpenAIEmbeddings model instance configured with the provided settings.
        """
        return AzureOpenAIEmbeddings(
            model=self.settings.model,
            azure_endpoint=self.settings.api_base,
            azure_deployment=self.settings.deployment,
            api_key=fetch_secret_key_value(self.settings.api_key),
            api_version=self.settings.api_version,
            chunk_size=16,
        )
