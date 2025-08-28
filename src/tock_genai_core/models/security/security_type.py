from typing import Annotated, Union

from pydantic import Field

from tock_genai_core.models.security.aws_secret_key import AwsSecretKey
from tock_genai_core.models.security.gcp_secret_key import GcpSecretKey
from tock_genai_core.models.security.raw_secret_key import RawSecretKey
from tock_genai_core.models.security.kube_secret_key import KubernetesSecretKey

SecretKey = Annotated[
    Union[RawSecretKey, AwsSecretKey, KubernetesSecretKey, GcpSecretKey],
    Field(discriminator="type"),
]
