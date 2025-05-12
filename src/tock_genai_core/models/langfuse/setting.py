# -*- coding: utf-8 -*-
"""
LangfuseSetting

Configuration settings for Langfuse integration.
This class defines the configuration required to connect to Langfuse.

Authors:
    * Baptiste Le Goff: baptiste.le-goff@arkea.com
    * Killian Mahé: killian.mahe@partnre.com
    * Luigi Bokalli: luigi.bokalli@partnre.com
    * Noé Chabanon: noe.chabanon@partnre.com
"""
from typing import Optional

from pydantic import BaseModel, Field

from tock_genai_core.models.security.security_type import SecretKey
from tock_genai_core.models.security.raw_secret_key import RawSecretKey


class LangfuseSetting(BaseModel):
    """
    Configuration settings for Langfuse integration.
    This class defines the configuration required to connect to Langfuse.

    Attributes
    ----------
    host: Optional[str]
        Langfuse host
    public_key: Optional[SecretKey]
        Langfuse public key used for authentication (default: None)
    secret_key: Optional[SecretKey]
        Langfuse secret key used for authentication (default: None)
    app_name: Optional[str]
        Metadata - Application name (default: None)
    user_id: Optional[str]
        ID of the user making the request (default: None)
    session_id: Optional[str]
        ID of the conversation session (default: None)
    """

    host: Optional[str] = Field(description="Langfuse host.")
    public_key: Optional[SecretKey] = Field(
        description="Langfuse public key used for authentication.",
        default=None,
        examples=[RawSecretKey(type="Raw", value="your-public-key")],
    )
    secret_key: Optional[SecretKey] = Field(
        description="Langfuse secret key used for authentication.",
        default=None,
        examples=[RawSecretKey(type="Raw", value="your-secret-key")],
    )
    app_name: Optional[str] = Field(description="Metadata - Application name.", default=None)
    user_id: Optional[str] = Field(description="ID of the user making the request.", default=None)
    session_id: Optional[str] = Field(description="ID of the conversation session.", default=None)
