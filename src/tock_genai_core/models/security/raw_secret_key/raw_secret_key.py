from typing import Literal

from pydantic import Field

from tock_genai_core.models.security.secret_key import BaseSecretKey
from tock_genai_core.models.security.secret_key_type import SecretKeyType


class RawSecretKey(BaseSecretKey):
    """
    A class for Raw Secret Key.
    Used to store a secret in its raw form.
    """

    type: Literal[SecretKeyType.RAW] = Field(
        description="The Secret Key type.",
        examples=[SecretKeyType.RAW],
        default=SecretKeyType.RAW,
    )
    value: str = Field(description="The secret value.", examples=["145d-ff455g-e4r5gf"], min_length=1)
