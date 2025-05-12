from tock_genai_core.models.llm import BaseLLMSetting, LLMProvider
from tock_genai_core.services.langchain.factory.factories import LLMFactory
from tock_genai_core.services.langchain.factory.llm import (
    AzureOpenAILLMFactory,
    TGIFactory,
    VllmFactory,
)


def get_llm_factory(settings: BaseLLMSetting) -> LLMFactory:
    """
    Retrieve the appropriate LLM factory based on the provider specified in the settings.

    Parameters
    ----------
    settings : BaseLLMSetting
        The settings for the LLM, including the provider type.

    Returns
    -------
    LLMFactory
        An instance of the corresponding LLM factory for the specified provider.
    """
    if settings.provider == LLMProvider.TGI:
        return TGIFactory(settings=settings)
    if settings.provider == LLMProvider.AzureOpenAI:
        return AzureOpenAILLMFactory(settings=settings)
    if settings.provider == LLMProvider.Vllm:
        return VllmFactory(settings=settings)
