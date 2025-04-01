from tock_genai_core.services.langchain.factory.factories import GuardrailFactory
from tock_genai_core.models.guardrail import BaseGuardrailSetting, GuardrailProvider
from tock_genai_core.services.langchain.factory.guardrail import (
    BloomzGuardrailFactory,
)


def get_guardrail_factory(settings: BaseGuardrailSetting) -> GuardrailFactory:
    """
    Retrieves the appropriate guardrail factory based on the provider specified in the settings.

    Parameters
    ----------
    settings : BaseGuardrailSetting
        The settings for the guardrail, including the provider type.

    Returns
    -------
    GuardrailFactory
        An instance of the corresponding guardrail factory for the specified provider.
    """
    if settings.provider == GuardrailProvider.BloomZ:
        return BloomzGuardrailFactory(settings=settings)
