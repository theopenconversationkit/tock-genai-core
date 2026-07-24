# -*- coding: utf-8 -*-
"""
PGVectorStoreSetting

Configuration settings for the PGVectorStore (langchain_postgres v2) vector database, an
alternative to PGVector (v1) with a one-physical-table-per-collection schema. Opt-in via
`provider=VectorDBProvider.PGVectorStore`; existing `PGVectorSetting`/`VectorDBProvider.PGVector`
consumers are unaffected.
"""
from typing import List, Literal, Optional
from pydantic import BaseModel, Field

from tock_genai_core.models.database.provider import VectorDBProvider
from tock_genai_core.models.database.pgvector.pgvector_db_setting import PGVectorSetting


class MetadataColumnSetting(BaseModel):
    """
    Describes one metadata column to create on a collection's physical table.

    Attributes
    ----------
    name: str
        The column name.
    data_type: str
        The SQL data type of the column (e.g. "TEXT", "INTEGER", "BOOLEAN").
    """

    name: str = Field(description="The column name.")
    data_type: str = Field(description="The SQL data type of the column (e.g. 'TEXT', 'INTEGER', 'BOOLEAN').")


class PGVectorStoreSetting(PGVectorSetting):
    """
    Configuration settings for the PGVectorStore vector database.

    Attributes
    ----------
    provider: Literal[VectorDBProvider.PGVectorStore]
        The vector store used (default: VectorDBProvider.PGVectorStore)
    common_metadata_columns: Optional[List[MetadataColumnSetting]]
        Metadata columns to create on every collection's table for this application, in addition
        to any custom fields declared per-collection via the metadata-fields mechanism. Callers
        of tock-genai-core define their own domain-specific list here (e.g. orchestrator_x260
        derives its list from its `EmbeddingCMetadata` model); tock-genai-core itself has no
        opinion on what these columns should be. Defaults to none.
    fts_column: Optional[str]
        If set, a PostgreSQL full-text-search GIN index is created on this column for every new
        collection's table (used for lexical/hybrid search). Left unset, no such index is
        created. Defaults to None.
    fts_language: str
        The `to_tsvector`/`to_tsquery` text-search configuration language used for `fts_column`'s
        index (e.g. "english", "french"). Only relevant when `fts_column` is set.
    """

    provider: Literal[VectorDBProvider.PGVectorStore] = Field(
        description="The vector store used.", default=VectorDBProvider.PGVectorStore
    )
    common_metadata_columns: Optional[List[MetadataColumnSetting]] = Field(
        description="Metadata columns to create on every collection's table for this application.",
        default=None,
    )
    fts_column: Optional[str] = Field(
        description="If set, a full-text-search GIN index is created on this column for every new "
        "collection's table.",
        default=None,
    )
    fts_language: str = Field(
        description="The text-search configuration language used for `fts_column`'s index.",
        default="english",
    )
