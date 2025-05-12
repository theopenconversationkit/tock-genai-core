# -*- coding: utf-8 -*-
"""
PGVectorSetting

Configuration settings for PGVector vector database.
This class defines the configuration for connecting to a PGVector database.

Authors:
    * Baptiste Le Goff: baptiste.le-goff@arkea.com
    * Killian Mahé: killian.mahe@partnre.com
    * Luigi Bokalli: luigi.bokalli@partnre.com
    * Noé Chabanon: noe.chabanon@partnre.com
"""
from typing import Literal, Optional
from pydantic import Field

from tock_genai_core.models.database.provider import VectorDBProvider
from tock_genai_core.models.database.setting import BaseVectorDBSetting
from tock_genai_core.models.security.security_type import SecretKey


class PGVectorSetting(BaseVectorDBSetting):
    """
    Configuration settings for PGVector vector database.
    This class defines the configuration for connecting to a PGVector database.

    Attributes
    ----------
    provider: Literal[VectorDBProvider.PGVector]
        The vector store used (default: VectorDBProvider.PGVector)
    username: SecretKey
        Database username (default: None)
    password: SecretKey
        Database password (default: None)
    db_name: str
        Database name (default: None)
    sslmode: Optional[str]
        The SSL mode used in the connection with the database  (default: require)
    namespace: str
        Name of the application in use
    """

    provider: Literal[VectorDBProvider.PGVector] = Field(
        description="The vector store used.", default=VectorDBProvider.PGVector
    )
    username: SecretKey = Field(description="Database username.", default=None)
    password: SecretKey = Field(description="Database password.", default=None)
    db_name: str = Field(description="Database name", default=None)
    sslmode: Optional[str] = Field(
        description="The SSL mode used in the connection with the database.", default="require"
    )
    namespace: str = Field(description="Name of the application in use")
