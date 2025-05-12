from langchain.base_language import BaseLanguageModel
from langchain_community.llms.huggingface_text_gen_inference import HuggingFaceTextGenInference

from tock_genai_core.services.langchain.factory.factories import LLMFactory
from tock_genai_core.models.llm import HuggingFaceTextGenInferenceLLMSetting


class TGIFactory(LLMFactory):
    """
    Factory class for creating Hugging Face Text Generation Inference (TGI) language models.
    This class is responsible for instantiating a `HuggingFaceTextGenInference` model using the settings
    defined in the `HuggingFaceTextGenInferenceLLMSetting` class.

    Attributes
    ----------
    settings : HuggingFaceTextGenInferenceLLMSetting
        The settings used to configure the `HuggingFaceTextGenInference` model.
    """

    settings: HuggingFaceTextGenInferenceLLMSetting

    def get_model(self) -> BaseLanguageModel:
        """
        Returns a HuggingFaceTextGenInference model instance configured with the provided settings.
        """
        return HuggingFaceTextGenInference(
            inference_server_url=self.settings.api_base,
            temperature=self.settings.temperature,
            repetition_penalty=self.settings.repetition_penalty,
            max_new_tokens=self.settings.max_new_tokens,
            streaming=self.settings.streaming,
        )
