# -*- coding: utf-8 -*-
"""
RawSecretKey

A class for Raw Secret Key.
Used to store a secret in its raw form.

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


class RawSecretKey(BaseSecretKey):
    """
    A class for Raw Secret Key.
    Used to store a secret in its raw form.

    Attributes
    ----------

    type: Literal[SecretKeyType.RAW]
        The Secret Key type (default: SecretKeyType.RAW )
    secret_name: str
        The secret value
    """

    type: Literal[SecretKeyType.RAW] = Field(
        description="The Secret Key type.",
        examples=[SecretKeyType.RAW],
        default=SecretKeyType.RAW,
    )
    secret: str = Field(description="The secret value.", examples=["145d-ff455g-e4r5gf"], min_length=1, alias="value")
