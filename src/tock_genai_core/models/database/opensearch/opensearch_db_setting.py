# -*- coding: utf-8 -*-
"""
OpenSearchSetting

Configuration settings for OpenSearch vector database.
This class defines the configuration for connecting to an OpenSearch vector database.

Authors:
    * Baptiste Le Goff: baptiste.le-goff@arkea.com
    * Killian Mahé: killian.mahe@partnre.com
    * Luigi Bokalli: luigi.bokalli@partnre.com
    * Noé Chabanon: noe.chabanon@partnre.com
"""
from typing import Literal

from pydantic import Field

from tock_genai_core.models.database.provider import VectorDBProvider
from tock_genai_core.models.database.setting import BaseVectorDBSetting
from tock_genai_core.models.security.security_type import SecretKey


class OpenSearchSetting(BaseVectorDBSetting):
    """
    Configuration settings for OpenSearch vector database.
    This class defines the configuration for connecting to an OpenSearch vector database.

    Attributes
    ----------
    provider: Literal[VectorDBProvider.OpenSearch]
        The vector store used (default: VectorDBProvider.OpenSearch)
    username: SecretKey
        Database username (default: None)
    password: SecretKey
        Database password (default: None)
    use_ssl: bool
        Use an SSL connection or not
    verify_certs: bool
        Verify certificates authenticity or not
    """

    provider: Literal[VectorDBProvider.OpenSearch] = Field(
        description="The vector store used.", default=VectorDBProvider.OpenSearch
    )
    username: SecretKey = Field(description="Database username.", default=None)
    password: SecretKey = Field(description="Database password.", default=None)
    use_ssl: bool = Field(description="Use an SSL connection or not.")
    verify_certs: bool = Field(description="Verify certificates authenticity or not.")
