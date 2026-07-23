from langchain.retrievers.document_compressors.base import BaseDocumentCompressor

from tock_genai_core.services.compressor import LLMRerank
from tock_genai_core.models.contextual_compressor import LLMCompressorSetting
from tock_genai_core.services.langchain.factory.factories import (
    CompressorFactory,
)


class LLMCompressorFactory(CompressorFactory):
    """
    Factory class for creating LLMRerank compressors.
    This class is responsible for instantiating a `LLMRerank` compressor using the settings defined in
    the `LLMCompressorSetting` class.

    Attributes
    ----------
    settings : LLMCompressorSetting
        The settings used to configure the `LLMRerank` compressor
    """

    settings: LLMCompressorSetting

    def get_compressor(self) -> BaseDocumentCompressor:
        """
        Returns a `LLMRerank` compressor instance configured with the provided settings.
        """
        return LLMRerank(
            provider = self.settings.provider,
            provider_settings= self.settings.provider_settings,
            min_score = self.settings.min_score,
            max_documents=self.settings.max_documents
        )
