# -*- coding: utf-8 -*-
"""
KubernetesSecretKey

A class for Kubernetes Secret Key.
Used to store the secret name managed in Kubernetes Secrets Manager.

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


class KubernetesSecretKey(BaseSecretKey):
    """
    A class for Kubernetes Secret Key.
    Used to store the secret name managed in Kubernetes Secrets Manager.

    Attributes
    ----------

    type: Literal[SecretKeyType.KUBERNETES_SECRET]
        The Secret Key type (default: SecretKeyType.KUBERNETES_SECRET )
    secret_name: str
        The secret name in Kubernetes
    """

    type: Literal[SecretKeyType.KUBERNETES_SECRET] = Field(
        description="The Secret Key type.",
        examples=[SecretKeyType.KUBERNETES_SECRET],
        default=SecretKeyType.KUBERNETES_SECRET,
    )
    secret_name: str = Field(
        description="The secret name in Kubernetes.",
        examples=["openaiapi_key"],
        min_length=1,
    )
