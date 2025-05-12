# -*- coding: utf-8 -*-
"""
VectorDBProvider

Enum for different vector database providers.
This class defines the available vector database providers.

Authors:
    * Baptiste Le Goff: baptiste.le-goff@arkea.com
    * Killian Mahé: killian.mahe@partnre.com
    * Luigi Bokalli: luigi.bokalli@partnre.com
    * Noé Chabanon: noe.chabanon@partnre.com
"""
from enum import Enum, unique


@unique
class VectorDBProvider(str, Enum):
    """
    Enum for different vector database providers.
    This class defines the available vector database providers.
    """

    OpenSearch = "OPENSEARCH"
    PGVector = "PGVECTOR"

    @classmethod
    def has_value(cls, value) -> bool:
        return value in cls._value2member_map_
