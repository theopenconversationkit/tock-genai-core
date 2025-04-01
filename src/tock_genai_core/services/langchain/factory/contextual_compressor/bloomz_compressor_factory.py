from langchain.retrievers.document_compressors.base import BaseDocumentCompressor

from tock_genai_core.services.compressor import BloomzRerank
from tock_genai_core.models.contextual_compressor import BloomZCompressorSetting
from tock_genai_core.services.langchain.factory.factories import (
    CompressorFactory,
)
from tock_genai_core.services.security.security_service import fetch_secret_key_value


class BloomzCompressorFactory(CompressorFactory):
    """
    Factory class for creating BloomzRerank compressors.
    This class is responsible for instantiating a `BloomzRerank` compressor using the settings defined in
    the `BloomZCompressorSetting` class.

    Attributes
    ----------
    settings : BloomZCompressorSetting
        The settings used to configure the `BloomzRerank` compressor
    """

    settings: BloomZCompressorSetting

    def get_compressor(self) -> BaseDocumentCompressor:
        """
        Returns a `BloomzRerank` compressor instance configured with the provided settings.
        """
        return BloomzRerank(
            min_score=self.settings.min_score,
            endpoint=self.settings.endpoint,
            max_documents=self.settings.max_documents,
            label=self.settings.label,
            api_key=fetch_secret_key_value(self.settings.api_key) if self.settings.api_key else None,
        )
