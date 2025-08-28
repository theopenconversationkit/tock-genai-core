# -*- coding: utf-8 -*-
"""
GCPSecretManagerClient

Minimal GCP Secret Manager client.
Used to fetch secrets from Google Cloud Secret Manager.

Author:
    * Louis-Marie Toudoire louis-marie.toudoire@partnre.com
"""

import json
import logging
from typing import Union, Optional

from google.api_core.exceptions import NotFound
from google.cloud import secretmanager
from google.auth import default as google_auth_default

logger = logging.getLogger(__name__)


class GCPSecretManagerClient:
    """Minimal GCP Secret Manager Client."""

    def __init__(self, project_id: Optional[str] = None):
        """
        Initialize the client.

        Parameters
        ----------
        project_id : Optional[str]
            The GCP project ID where the secrets are stored.
            - If provided: use it directly (same approach as Orchestrator).
            - If not provided: try to auto-detect from Google application credentials.
        """
        if project_id:
            # Case 1: project_id explicitly provided (e.g. env var GCP_PROJECT_ID or orchestrator config)
            self.project_id = project_id
            self.client = secretmanager.SecretManagerServiceClient()
        else:
            # Case 2: auto-detection from GOOGLE_APPLICATION_CREDENTIALS or default credentials
            creds, detected_project_id = google_auth_default()
            if not detected_project_id:
                raise RuntimeError(
                    "Unable to determine the project_id. "
                    "Either set GCP_PROJECT_ID or configure GOOGLE_APPLICATION_CREDENTIALS."
                )
            self.project_id = detected_project_id
            self.client = secretmanager.SecretManagerServiceClient(credentials=creds)

    def get_secret(self, secret_name: str) -> Union[str, dict, None]:
        """
        Retrieve individual secret by name, using the access_secret_version API.

        Parameters
        ----------
        secret_name : str
            The name of the secret to be fetched.

        Returns
        -------
        Union[str, dict, None]
            The secret as a raw string, as a dictionary if the content is JSON, or None if the secret has no payload.
        """
        resource_name = f"projects/{self.project_id}/secrets/{secret_name}/versions/latest"

        try:
            response = self.client.access_secret_version(name=resource_name)
            secret_string = response.payload.data.decode("UTF-8")
            if not secret_string:
                logger.warning(f"Secret {secret_name} retrieved but has no payload.")
                return None

            try:
                return json.loads(secret_string)
            except json.JSONDecodeError:
                return secret_string

        except NotFound:
            logger.error(f"The requested secret {secret_name} was not found in project {self.project_id}.")
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving secret {secret_name}: {e}")
            raise
