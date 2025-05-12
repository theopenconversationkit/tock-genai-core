from langchain.base_language import BaseLanguageModel
from langchain_openai.chat_models import AzureChatOpenAI

from tock_genai_core.models.llm import AzureOpenAILLMSetting
from tock_genai_core.services.langchain.factory.factories import LLMFactory
from tock_genai_core.services.security.security_service import fetch_secret_key_value


class AzureOpenAILLMFactory(LLMFactory):
    """
    Factory class for creating OpenAI language models.
    This class is responsible for instantiating an `AzureChatOpenAI` object using the settings defined in the
    `OpenAILLMSetting` class.

    Attributes
    ----------
    settings : OpenAILLMSetting
        The settings used to configure the `AzureChatOpenAI` model.
    """

    settings: AzureOpenAILLMSetting

    def get_model(self) -> BaseLanguageModel:
        """
        Returns an AzureChatOpenAI model instance configured with the provided settings.
        """
        return AzureChatOpenAI(
            model=self.settings.model,
            deployment_name=self.settings.deployment,
            azure_endpoint=self.settings.api_base,
            api_key=fetch_secret_key_value(self.settings.api_key),
            api_version=self.settings.api_version,
            temperature=self.settings.temperature,
        )
