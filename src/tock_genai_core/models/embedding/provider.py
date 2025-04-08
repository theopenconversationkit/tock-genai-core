from enum import Enum, unique


@unique
class EMProvider(str, Enum):
    """
    Enum for embedding model providers.
    This class defines the available embedding model providers.
    """

    BloomZ = "BloomzEmbeddings"
    AzureOpenAI = "AzureOpenAI"
    Vllm = "Vllm"

    @classmethod
    def has_value(cls, value) -> bool:
        return value in cls._value2member_map_
