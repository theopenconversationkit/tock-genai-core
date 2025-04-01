from tock_genai_core.services.langchain.factory.factories import CompressorFactory
from tock_genai_core.services.langchain.factory.contextual_compressor import (
    BloomzCompressorFactory,
)
from tock_genai_core.models.contextual_compressor import (
    BaseCompressorSetting,
    ContextualCompressorProvider,
)


def get_compressor_factory(settings: BaseCompressorSetting) -> CompressorFactory:
    """
    Retrieves the appropriate compressor factory based on the provider specified in the settings.

    Parameters
    ----------
    settings : BaseCompressorSetting
        The settings for the compressor, including the provider type.

    Returns
    -------
    CompressorFactory
        An instance of the corresponding compressor factory for the specified provider.
    """
    if settings.provider == ContextualCompressorProvider.BloomZ:
        return BloomzCompressorFactory(settings=settings)
