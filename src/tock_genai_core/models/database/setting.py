# -*- coding: utf-8 -*-
"""
BaseVectorDBSetting

Base class for settings related to vector database configurations. This class holds the basic configuration
parameters for a vector database.

Authors:
    * Baptiste Le Goff: baptiste.le-goff@arkea.com
    * Killian Mahé: killian.mahe@partnre.com
    * Luigi Bokalli: luigi.bokalli@partnre.com
    * Noé Chabanon: noe.chabanon@partnre.com
"""
from typing import Optional

from pydantic import BaseModel, Field

from tock_genai_core.models.database.provider import VectorDBProvider


class BaseVectorDBSetting(BaseModel):
    """
    Base class for settings related to vector database configurations. This class holds the basic configuration
    parameters for a vector database.

    Attributes
    ----------
    index: Optional[str]
        Index name (default: None)
    provider: VectorDBProvider
        The vector store used
    db_url: str
        The URL of the database
    """

    index: Optional[str] = Field(description="Index name", default=None)
    provider: VectorDBProvider = Field(description="The vector store used.")
    db_url: str = Field(description="The URL of the database.")
