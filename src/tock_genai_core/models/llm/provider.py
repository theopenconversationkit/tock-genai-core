from enum import Enum, unique


@unique
class LLMProvider(str, Enum):
    """
    Enum for LLM providers.
    This class defines the available LLM providers.
    """

    TGI = "HuggingFaceTextGenInference"
    OpenAI = "OpenAI"
    Vllm = "Vllm"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
