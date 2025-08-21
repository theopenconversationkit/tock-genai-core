# -*- coding: utf-8 -*-
"""
GcpSecretKey

A class for GCP Secret Key.
Used to store the secret name managed in GCP Secrets Manager.

Authors:
    * Baptiste Le Goff: baptiste.le-goff@arkea.com
    * Killian Mahé: killian.mahe@partnre.com
    * Luigi Bokalli: luigi.bokalli@partnre.com
    * Noé Chabanon: noe.chabanon@partnre.com
"""
from typing import Literal

from pydantic import Field

from tock_genai_core.models.security.secret_key import BaseSecretKey
from tock_genai_core.models.security.secret_key_type import SecretKeyType


class GcpSecretKey(BaseSecretKey):
    """
    A class for GCP Secret Key.
    Used to store the secret name managed in GCP Secret Manager.

    Attributes
    ----------
    type: Literal[SecretKeyType.GCP_SECRETS_MANAGER]
        The Secret Key type (default: SecretKeyType.GCP_SECRETS_MANAGER )
    secret_name: str
        The secret name managed in GCP Secret Manager
    """

    type: Literal[SecretKeyType.GCP_SECRETS_MANAGER] = Field(
        description="The Secret Key type.",
        examples=[SecretKeyType.GCP_SECRETS_MANAGER],
        default=SecretKeyType.GCP_SECRETS_MANAGER,
    )
    secret_name: str = Field(
        description="The secret name managed in GCP Secret Manager.",
        examples=["PROD/App/openaiapi_key"],
        min_length=1,
    )
