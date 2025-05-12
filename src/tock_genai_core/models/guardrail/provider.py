# -*- coding: utf-8 -*-
"""
GuardrailProvider

Enum for guardrail model providers.
This class defines the available guardrail model providers.

Authors:
    * Baptiste Le Goff: baptiste.le-goff@arkea.com
    * Killian Mahé: killian.mahe@partnre.com
    * Luigi Bokalli: luigi.bokalli@partnre.com
    * Noé Chabanon: noe.chabanon@partnre.com
"""
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
