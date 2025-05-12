# -*- coding: utf-8 -*-
"""
AwsSecretKey

A class for AWS Secret Key.
Used to store the secret name managed in AWS Secrets Manager.

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


class AwsSecretKey(BaseSecretKey):
    """
    A class for AWS Secret Key.
    Used to store the secret name managed in AWS Secrets Manager.

    Attributes
    ----------

    type: Literal[SecretKeyType.AWS_SECRETS_MANAGER]
        The Secret Key type (default: SecretKeyType.AWS_SECRETS_MANAGER )
    secret_name: str
        The secret name managed in AWS Secrets Manager
    """

    type: Literal[SecretKeyType.AWS_SECRETS_MANAGER] = Field(
        description="The Secret Key type.",
        examples=[SecretKeyType.AWS_SECRETS_MANAGER],
        default=SecretKeyType.AWS_SECRETS_MANAGER,
    )
    secret_name: str = Field(
        description="The secret name managed in AWS Secrets Manager.",
        examples=["PROD/App/openaiapi_key"],
        min_length=1,
    )
