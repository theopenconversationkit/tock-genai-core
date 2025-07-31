import logging
from typing import Union

from langfuse.langchain import CallbackHandler
from langfuse import Langfuse

from tock_genai_core.models.security.security_type import SecretKey
from tock_genai_core.models.langfuse.setting import LangfuseSetting
from tock_genai_core.services.security.security_service import fetch_secret_key_value


logger = logging.getLogger(__name__)

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


class LangfuseHandler:
    """
    A handler class for interacting with the Langfuse service to manage API keys and set up callback handling.
    This class is responsible for managing the configuration of Langfuse service, including the API keys
    (public and secret) and the host URL.

    Attributes
    ----------
    public_key : str
        The public API key used to authenticate with Langfuse.
    secret_key : str
        The secret API key used to authenticate with Langfuse.
    host : str
        The host URL of the Langfuse service.

    Methods
    -------
    exists() -> bool
        Returns whether the public API key is provided (i.e., if the handler is properly configured).
    get_handler() -> CallbackHandler
        Returns a `CallbackHandler` instance configured with the Langfuse API keys and host.
    """

    config: Union[LangfuseSetting, None] = None

    def __init__(
        self,
        public_key: SecretKey,
        secret_key: SecretKey,
        host: str,
    ):
        self.public_key = fetch_secret_key_value(public_key)
        self.secret_key = fetch_secret_key_value(secret_key)
        self.host = host

    def exists(self) -> bool:
        """
        Checks whether the public API key is provided and valid.

        Returns
        -------
        bool
            Returns True if the public key is not None, indicating that the handler is properly configured.
            Otherwise, returns False.
        """
        return True if self.public_key is not None else False

    def get_handler(self) -> CallbackHandler:
        """
        Returns a `CallbackHandler` instance configured with the Langfuse API keys and host.
        This method is used to initialize a handler that can interact with Langfuse service for callback handling.

        Returns
        -------
        CallbackHandler
            A configured `CallbackHandler` instance.
        """
        Langfuse(public_key=self.public_key, secret_key=self.secret_key, host=self.host)
        return CallbackHandler()
