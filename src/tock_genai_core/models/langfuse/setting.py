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
from typing import Optional, Dict, Any

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
    metadata: Optional[Dict[str, Any]]
        Optional metadata containing Langfuse-specific fields such as:
            - "langfuse_session_id": str — ID of the session to associate with the trace.
            - "langfuse_user_id": str — ID of the user to associate with the trace.
            - "langfuse_tags": list[str] — Tags to associate with the trace.
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
    metadata: Optional[Dict[str, Any]] = Field(description="Associated metadata", default={})
