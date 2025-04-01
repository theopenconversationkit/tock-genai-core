from typing import Literal
from pydantic import Field

from tock_genai_core.models.database.provider import RelationalDBProvider
from tock_genai_core.models.database.setting import BaseRelationalDBSetting
from tock_genai_core.models.security.security_type import SecretKey


class PostgresSetting(BaseRelationalDBSetting):
    """
    Configuration settings for PostgreSQL relational database.
    This class defines the configuration for connecting to a PostgreSQL relational database.
    """

    provider: Literal[RelationalDBProvider.PostgreSQL] = Field(description="The vector store used.")
    username: SecretKey = Field(description="Database username.", default=None)
    password: SecretKey = Field(description="Database password.", default=None)
    db_name: str = Field(description="Database name", default=None)
