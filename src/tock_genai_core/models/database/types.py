from typing import Annotated, Union

from pydantic import Field

from tock_genai_core.models.database.opensearch.opensearch_db_setting import (
    OpenSearchSetting,
)
from tock_genai_core.models.database.postgres.pgvector_db_setting import PGVectorSetting
from tock_genai_core.models.database.postgres.postgres_db_setting import PostgresSetting

# DBSetting is a type annotation that defines a union of possible database settings.
# The settings are determined by the value of the "provider" field, which acts as a discriminator.
DBSetting = Annotated[Union[OpenSearchSetting, PostgresSetting, PGVectorSetting], Field(discriminator="provider")]
