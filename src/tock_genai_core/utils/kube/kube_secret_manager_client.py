# -*- coding: utf-8 -*-
"""
KubeSecretManagerClient

Minimal Kubernetes Secret Manager client.
Used to fetch secrets from a Kubernetes cluster.

Author:
    * Alix Machard alix.machard@partnre.com
"""

import base64
import json
import logging
from typing import Union, Optional

from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

logger = logging.getLogger(__name__)


class KubeSecretManagerClient:
    """Minimal Kubernetes Secret Manager Client."""

    def __init__(self, namespace: str = "default"):
        """Initialize client

        Args:
            namespace (str, optional): Namespace from which secrets will be retrieved. Defaults to "default".
        """

        try:
            config.load_incluster_config()
            logger.info("Using in-cluster Kubernetes configuration.")
        except Exception:
            config.load_kube_config()
            logger.info("Using local kubeconfig.")

        self.api = client.CoreV1Api()
        self.default_namespace = namespace

    def get_secret(
        self, secret_name: str, namespace: Optional[str] = None, secret_key: Optional[str] = None
    ) -> Union[str, dict, None]:
        """Retrieve an individual secret from Kubernetes. Will try to parse it as JSON.

        Args:
            secret_name (str): Name of the secret to fetch.
            namespace (str, optional): Override namespace for this lookup. Defaults to client's namespace.
            secret_key (str, optional): Specific key to extract from the secret data.
                If not provided, the first key in the secret data will be used.

        Returns:
            Union[str, dict, None]: Decoded secret as dict if JSON, string if text, None if empty

        Raises:
            ApiException: If the secret cannot be retrieved from Kubernetes.
            ValueError: If the specified secret_key is not found in the secret data.
        """

        final_namespace = namespace or self.default_namespace

        try:
            secret = self.api.read_namespaced_secret(name=secret_name, namespace=final_namespace)
        except ApiException as e:
            if e.status == 404:
                logger.error(f"Secret '{secret_name}' not found in namespace '{final_namespace}'.")
                raise
            logger.error(f"Unexpected error retrieving secret {secret_name} in '{final_namespace}': {e}")
            raise

        if not secret.data:
            logger.warning(f"Secret '{secret_name}' retrieved but has no payload.")
            return None

        # Extract the appropriate key from secret data
        if secret_key:
            if secret_key not in secret.data:
                logger.error(
                    f"Specified secret key not found in Kubernetes secret '{secret_name}'."
                )
                raise ValueError(
                    f"Specified secret key not found in Kubernetes secret '{secret_name}'."
                )
            b64_value = secret.data[secret_key]
        else:
            # Fallback to first key (backward compatible behavior)
            key, b64_value = next(iter(secret.data.items()))
            logger.debug(f"No secret_key specified, using first key '{key}' from secret '{secret_name}'")

        decoded = base64.b64decode(b64_value).decode("utf-8")

        if not decoded:
            return None

        # Try JSON decode
        try:
            return json.loads(decoded)
        except json.JSONDecodeError:
            return decoded
