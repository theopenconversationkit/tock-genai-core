# -*- coding: utf-8 -*-
"""
LLMProvider

Enum for LLM providers.
This class defines the available LLM providers.

Authors:
    * Baptiste Le Goff: baptiste.le-goff@arkea.com
    * Killian Mahé: killian.mahe@partnre.com
    * Luigi Bokalli: luigi.bokalli@partnre.com
    * Noé Chabanon: noe.chabanon@partnre.com
"""
from enum import Enum, unique


@unique
class LLMProvider(str, Enum):
    """
    Enum for LLM providers.
    This class defines the available LLM providers.
    """

    TGI = "HuggingFaceTextGenInference"
    AzureOpenAI = "AzureOpenAI"
    Vllm = "Vllm"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
