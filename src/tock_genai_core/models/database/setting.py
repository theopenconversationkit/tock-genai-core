from typing import Optional

from pydantic import BaseModel, Field

from tock_genai_core.models.database.provider import VectorDBProvider, RelationalDBProvider


class BaseVectorDBSetting(BaseModel):
    """
    Base class for settings related to vector database configurations. This class holds the basic configuration
    parameters for a vector database.
    """

    index: Optional[str] = Field(description="Index name", default=None)
    provider: VectorDBProvider = Field(description="The vector store used.")
    db_url: str = Field(description="The URL of the database.")


class BaseRelationalDBSetting(BaseModel):
    """
    Base class for settings related to relational database configurations. This class holds the basic
    configuration parameters for a relational database.
    """

    index: Optional[str] = Field(description="Index name", default=None)
    provider: RelationalDBProvider = Field(description="The database used.")
    db_url: str = Field(description="The URL of the database.")
