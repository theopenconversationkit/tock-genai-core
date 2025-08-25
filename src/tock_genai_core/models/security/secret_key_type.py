# -*- coding: utf-8 -*-
"""
SecretKeyType

Enumeration to list Secret Key types

Authors:
    * Baptiste Le Goff: baptiste.le-goff@arkea.com
    * Killian Mahé: killian.mahe@partnre.com
    * Luigi Bokalli: luigi.bokalli@partnre.com
    * Noé Chabanon: noe.chabanon@partnre.com
"""
from enum import Enum, unique


@unique
class SecretKeyType(str, Enum):
    """Enumeration to list Secret Key types"""

    RAW = "Raw"
    AWS_SECRETS_MANAGER = "AwsSecretsManager"
    KUBERNETES_SECRET = "KubeSecret"
    GCP_SECRETS_MANAGER = "GcpSecretManager"
