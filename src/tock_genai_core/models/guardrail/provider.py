from enum import Enum, unique


@unique
class GuardrailProvider(str, Enum):
    """
    Enum for guardrail model providers.
    This class defines the available guardrail model providers.
    """

    BloomZ = "BloomzGuardrail"

    @classmethod
    def has_value(cls, value) -> bool:
        return value in cls._value2member_map_
