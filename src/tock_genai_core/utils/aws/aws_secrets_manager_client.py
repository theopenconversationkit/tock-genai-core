# -*- coding: utf-8 -*-
"""
AWSSecretsManagerClient

Minimal AWS Secrets Manager client.
Used to fetch secrets from AWS Secrets Manager.

Author:
    * Louis-Marie Toudoire louis-marie.toudoire@partnre.com
"""

import json
import logging
from typing import Union

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class AWSSecretsManagerClient:
    """AWS Secrets Manager Client."""

    def __init__(self):
        self.client = boto3.client(service_name="secretsmanager")

    def get_secret(self, secret_name: str) -> Union[str, dict, None]:
        """
        Retrieve individual secret by name, using the get_secret_value API.

        Parameters
        ----------
        secret_name : str
            The name of the secret to be fetched.

        Returns
        -------
        Union[str, dict, None]
        The secret as a raw string, as a dictionary if the secret is JSON, or None if the secret is empty.

        Raises
        ------
        ClientError
            If AWS Secrets Manager returns an error.
        Exception
            For any other unexpected error.
        """
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            secret_string = response.get("SecretString")
            if secret_string is None:
                logger.warning(f"Secret {secret_name} retrieved but has no SecretString field.")
                return None

            # Try to parse as JSON, else return raw string
            try:
                return json.loads(secret_string)
            except json.JSONDecodeError:
                return secret_string

        except ClientError as e:
            logger.error(f"Error retrieving secret {secret_name}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving secret {secret_name}: {e}")
            raise
