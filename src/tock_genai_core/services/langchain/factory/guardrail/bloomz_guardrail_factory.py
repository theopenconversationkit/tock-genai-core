from langchain_core.output_parsers import BaseOutputParser

from tock_genai_core.models.guardrail import BloomZGuardrailSetting
from tock_genai_core.services.langchain.factory.factories import (
    GuardrailFactory,
)
from tock_genai_core.services.guardrail import BloomzGuardrailOutputParser
from tock_genai_core.services.security.security_service import fetch_secret_key_value


class BloomzGuardrailFactory(GuardrailFactory):
    """
    Factory class for creating BloomzGuardrailOutputParser instances.
    This class is responsible for instantiating a `BloomzGuardrailOutputParser` object using the settings
    defined in the `BloomZGuardrailSetting` class.

    Attributes
    ----------
    settings : BloomZGuardrailSetting
        The settings used to configure the BloomzGuardrailOutputParser.
    """

    settings: BloomZGuardrailSetting

    def get_parser(self) -> BaseOutputParser:
        """
        Returns a BloomzGuardrailOutputParser instance configured with the provided settings.
        """
        return BloomzGuardrailOutputParser(
            max_score=self.settings.max_score,
            endpoint=self.settings.api_base,
            api_key=fetch_secret_key_value(self.settings.api_key) if self.settings.api_key else None,
        )
