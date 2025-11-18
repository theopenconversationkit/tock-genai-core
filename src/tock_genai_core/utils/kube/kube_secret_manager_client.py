# -*- coding: utf-8 -*-
"""
KubeSecretManagerClient

Minimal Kubernetes Secret Manager client.
Used to fetch secrets from a Kubernetes cluster.

Author:
    * Adapted for kube integration
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
        self.namespace = namespace

    def get_secret(self, secret_name: str) -> Union[str, dict, None]:
        """Retrieve an individual secret from Kubernetes.

        Args:
            secret_name (str): Name of the secret to fetch.

        Returns:
            Union[str, dict, None]: Decoded secret as dict if JSON, string if text, None if empty
        """
        try:
            secret = self.api.read_namespaced_secret(name=secret_name, namespace=self.namespace)
        except ApiException as e:
            if e.status == 404:
                logger.error(f"Secret '{secret_name}' not found in namespace '{self.namespace}'.")
                raise
            logger.error(f"Unexpected error retrieving secret {secret_name}: {e}")
            raise

        if not secret.data:
            logger.warning(f"Secret '{secret_name}' retrieved but has no payload.")
            return None

        # Kubernetes can store multiple key/value pairs → we assume 1 primary entry
        if len(secret.data) > 1:
            logger.warning(f"Secret '{secret_name}' contains multiple keys. " f"Returning the first one.")

        key, b64_value = next(iter(secret.data.items()))
        decoded = base64.b64decode(b64_value).decode("utf-8")

        if not decoded:
            return None

        # Try JSON decode
        try:
            return json.loads(decoded)
        except json.JSONDecodeError:
            return decoded
