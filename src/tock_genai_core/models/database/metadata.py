from pydantic import BaseModel


class MetadataFilter(BaseModel):
    """
    Represents a filter for metadata. This class defines a filter that can be applied to metadata.
    """

    field: str
    value: str | dict
