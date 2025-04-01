from enum import Enum, unique


@unique
class ContextualCompressorProvider(str, Enum):
    """
    Enum for contextual compressor providers.
    This class defines available providers for contextual compression.
    """

    BloomZ = "BloomzRerank"

    @classmethod
    def has_value(cls, value) -> bool:
        return value in cls._value2member_map_
