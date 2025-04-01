from enum import Enum, unique


@unique
class VectorDBProvider(str, Enum):
    """
    Enum for different vector database providers.
    This class defines the available vector database providers.
    """

    OpenSearch = "OPENSEARCH"
    PGVector = "PGVECTOR"

    @classmethod
    def has_value(cls, value) -> bool:
        return value in cls._value2member_map_


@unique
class RelationalDBProvider(str, Enum):
    """
    Enum for relational database providers.
    This class defines the available relational database providers.
    """

    PostgreSQL = "POSTGRESQL"

    @classmethod
    def has_value(cls, value) -> bool:
        return value in cls._value2member_map_
