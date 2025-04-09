from tock_genai_core.models.embedding import BaseEMSetting, EMProvider
from tock_genai_core.services.langchain.factory.factories import EMFactory
from tock_genai_core.services.langchain.factory.embedding import BloomzFactory, AzureOpenAIEMFactory, VLLMEMFactory


def get_em_factory(settings: BaseEMSetting) -> EMFactory:
    """
    Retrieves the appropriate embedding factory based on the provider specified in the settings.

    Parameters
    ----------
    settings : BaseEMSetting
        The settings for the embedding model, including the provider type.

    Returns
    -------
    EMFactory
        An instance of the corresponding embedding factory for the specified provider.
    """
    if settings.provider == EMProvider.BloomZ:
        return BloomzFactory(settings=settings)
    if settings.provider == EMProvider.AzureOpenAI:
        return AzureOpenAIEMFactory(settings=settings)
    if settings.provider == EMProvider.Vllm:
        return VLLMEMFactory(settings=settings)
