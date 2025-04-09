# -*- coding: utf-8 -*-
"""
ContextualCompressorProvider

Enum for contextual compressor providers.
This class defines available providers for contextual compression.

Authors:
    * Baptiste Le Goff: baptiste.le-goff@arkea.com
    * Killian Mahé: killian.mahe@partnre.com
    * Luigi Bokalli: luigi.bokalli@partnre.com
    * Noé Chabanon: noe.chabanon@partnre.com
"""
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
