from pydantic import BaseModel, Field

from tock_genai_core.models.security.secret_key_type import SecretKeyType


class BaseSecretKey(BaseModel):
    """A base class for Secret Key."""

    type: SecretKeyType = Field(description="The Secret Key type.", examples=[SecretKeyType.AWS_SECRETS_MANAGER])
