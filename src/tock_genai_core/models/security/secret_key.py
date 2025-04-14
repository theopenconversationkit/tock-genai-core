# -*- coding: utf-8 -*-
"""
BaseSecretKey

A base class for Secret Key

Authors:
    * Baptiste Le Goff: baptiste.le-goff@arkea.com
    * Killian Mahé: killian.mahe@partnre.com
    * Luigi Bokalli: luigi.bokalli@partnre.com
    * Noé Chabanon: noe.chabanon@partnre.com
"""
from pydantic import BaseModel, Field

from tock_genai_core.models.security.secret_key_type import SecretKeyType


class BaseSecretKey(BaseModel):
    """
    A base class for Secret Key.

    Attributes
    ----------

    type: SecretKeyType
        The Secret Key type (default: [SecretKeyType.AWS_SECRETS_MANAGER])
    """

    type: SecretKeyType = Field(description="The Secret Key type.", examples=[SecretKeyType.AWS_SECRETS_MANAGER])
