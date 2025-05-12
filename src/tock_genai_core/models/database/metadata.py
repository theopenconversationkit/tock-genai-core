# -*- coding: utf-8 -*-
"""
MetadataFilter

Represents a filter for metadata. This class defines a filter that can be applied to metadata.

Authors:
    * Baptiste Le Goff: baptiste.le-goff@arkea.com
    * Killian Mahé: killian.mahe@partnre.com
    * Luigi Bokalli: luigi.bokalli@partnre.com
    * Noé Chabanon: noe.chabanon@partnre.com
"""
from pydantic import BaseModel


class MetadataFilter(BaseModel):
    """
    Represents a filter for metadata. This class defines a filter that can be applied to metadata.
    """

    field: str
    value: str | dict
