from langchain.embeddings.base import Embeddings

from tock_genai_core.models.embedding import BloomZEMSetting
from tock_genai_core.services.embedding import BloomzEmbeddings
from tock_genai_core.services.langchain.factory.factories import EMFactory
from tock_genai_core.services.security.security_service import fetch_secret_key_value


class BloomzFactory(EMFactory):
    """
    Factory class for creating BloomzEmbeddings instances.
    This class is responsible for instantiating a `BloomzEmbeddings` object using the settings defined in the
    `BloomZEMSetting` class.

    Attributes
    ----------
    settings : BloomZEMSetting
        The settings used to configure the BloomzEmbeddings model.
    """

    settings: BloomZEMSetting

    def get_model(self) -> Embeddings:
        """
        Returns a BloomzEmbeddings model instance configured with the provided settings.
        """
        return BloomzEmbeddings(
            model=self.settings.model,
            pooling=self.settings.pooling,
            api_base=self.settings.api_base,
            api_key=fetch_secret_key_value(self.settings.api_key) if self.settings.api_key else None,
        )
