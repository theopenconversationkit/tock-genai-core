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

    def get_secret(self, secret_name: str, namespace: Optional[str] = None) -> Union[str, dict, None]:
        """Retrieve an individual secret from Kubernetes. Will try to parse it as JSON.

        Args:
            secret_name (str): Name of the secret to fetch.
            namespace (str, optional): Override namespace for this lookup. Defaults to client's namespace.

        Returns:
            Union[str, dict, None]: Decoded secret as dict if JSON, string if text, None if empty
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

        key, b64_value = next(iter(secret.data.items()))
        decoded = base64.b64decode(b64_value).decode("utf-8")

        if not decoded:
            return None

        # Try JSON decode
        try:
            return json.loads(decoded)
        except json.JSONDecodeError:
            return decoded
