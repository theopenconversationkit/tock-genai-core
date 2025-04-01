from langchain.base_language import BaseLanguageModel

from langchain_community.llms.vllm import VLLMOpenAI

from tock_genai_core.models.llm import VllmSetting
from tock_genai_core.services.langchain.factory.factories import LLMFactory
from tock_genai_core.services.security.security_service import fetch_secret_key_value


class VllmFactory(LLMFactory):
    """
    Factory class for creating VLLM (Variable Language Model) language models.
    This class is responsible for instantiating a `VLLMOpenAI` model using the settings defined in the
    `VllmSetting` class.

    Attributes
    ----------
    settings : VllmSetting
        The settings used to configure the `VLLMOpenAI` model.
    """

    settings: VllmSetting

    def get_model(self) -> BaseLanguageModel:
        """
        Returns a VLLMOpenAI model instance configured with the provided settings.
        """
        return VLLMOpenAI(
            model_name=self.settings.model,
            openai_api_key=fetch_secret_key_value(self.settings.api_key) if self.settings.api_key else "EMPTY",
            openai_api_base=self.settings.api_base,
            max_tokens=self.settings.max_new_tokens,
            temperature=self.settings.temperature,
            model_kwargs=self.settings.additional_model_kwargs,
            default_headers=(
                {"Authentication": f"Bearer {fetch_secret_key_value(self.settings.api_key)}"}
                if self.settings.api_key
                else {}
            ),
        )
