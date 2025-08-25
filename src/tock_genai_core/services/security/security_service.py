import os
from typing import Optional, Union, Dict

from tock_genai_core.models.security.gcp_secret_key import GcpSecretKey
from tock_genai_core.models.security.security_type import SecretKey
from tock_genai_core.models.security.raw_secret_key import RawSecretKey
from tock_genai_core.models.security.aws_secret_key import AwsSecretKey
from tock_genai_core.models.security.kube_secret_key import KubernetesSecretKey
from tock_genai_core.utils.aws.aws_secrets_manager_client import AWSSecretsManagerClient
from tock_genai_core.utils.gcp.gcp_secret_manager_client import GCPSecretManagerClient


def get_nested_value(data_dict, keys_str):
    """
    Retrieves the value from a nested dictionary using a string of keys separated by dots.

    Parameters
    ----------
    data_dict : dict
        The dictionary from which the value will be retrieved.
    keys_str : str
        A string representing the path of keys to access the nested value, with keys separated by dots.

    Returns
    -------
    The value found at the specified path in the dictionary. If any key is not found, an error will be raised.
    """
    keys = keys_str.split(".")
    value = data_dict
    for key in keys:
        value = value[key]
    return value


def fetch_secret_key_value(secret_key: SecretKey) -> Optional[Union[str, Dict[str, str]]]:
    """
    Fetches the value of a secret key based on its type.

    Parameters
    ----------
    secret_key : SecretKey
        The secret key whose value is to be retrieved.

    Returns
    -------
    Optional[Union[str, Dict[str, str]]]
        The value of the secret key, which can either be a string or a dictionary.

    Raises
    ------
    NotImplementedError
        If the secret key type is not yet implemented (e.g. KubernetesSecretKey).
    RuntimeError
        If the GCP project_id cannot be determined.
    """
    if isinstance(secret_key, RawSecretKey):
        return secret_key.secret
    elif isinstance(secret_key, AwsSecretKey):
        return AWSSecretsManagerClient().get_secret(secret_key.secret_name)
    elif isinstance(secret_key, KubernetesSecretKey):
        raise NotImplementedError()
    elif isinstance(secret_key, GcpSecretKey):
        project_id = os.getenv("GCP_PROJECT_ID")  # Will be None if not set
        return GCPSecretManagerClient(project_id=project_id).get_secret(secret_key.secret_name)
