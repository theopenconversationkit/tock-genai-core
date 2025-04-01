from enum import Enum, unique


@unique
class SecretKeyType(str, Enum):
    """Enumeration to list Secret Key types"""

    RAW = "Raw"
    AWS_SECRETS_MANAGER = "AwsSecretsManager"
    KUBERNETES_SECRET = "KubeSecret"
