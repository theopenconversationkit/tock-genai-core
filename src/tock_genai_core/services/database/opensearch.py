import logging

from opensearchpy import OpenSearch

from tock_genai_core.models.database.opensearch.opensearch_db_setting import (
    OpenSearchSetting,
)
from tock_genai_core.services.security.security_service import fetch_secret_key_value


logger = logging.getLogger(__name__)

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


def get_db_client(db_settings: OpenSearchSetting) -> OpenSearch:
    """
    Create an OpenSearch client using the provided database settings.

    Parameters
    ----------
    db_settings : OpenSearchSetting
        The settings for connecting to the OpenSearch database.

    Returns
    -------
    OpenSearch
        An OpenSearch client instance configured with the provided settings.
    """
    return OpenSearch(
        hosts=db_settings.db_url,
        http_auth=(fetch_secret_key_value(db_settings.username), fetch_secret_key_value(db_settings.password)),
        use_ssl=db_settings.use_ssl,
        verify_certs=db_settings.verify_certs,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
    )
