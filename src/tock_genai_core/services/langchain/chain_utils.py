from fastapi import HTTPException

from tock_genai_core.routes.requests import requests
from tock_genai_core.models.database.provider import VectorDBProvider


def get_base_search_kwargs(query: requests.RagQuery | requests.SearchRequest):
    """
    Returns the base search arguments for a retriever based on the provided query parameters.

    Parameters
    ----------
    query : requests.RagQuery | requests.SearchRequest
        The query object containing the parameters for the search.

    Returns
    -------
    dict
        A dictionary of search arguments (`search_kwargs`) that can be used in a retriever.

    Raises
    ------
    HTTPException
        If the vector store provider is unsupported, an HTTPException with status code 422 is raised.
    """
    search_kwargs = {"k": query.k}
    if query.metadata_filter:
        if query.db_settings.provider == VectorDBProvider.OpenSearch:
            search_kwargs["filter"] = {
                "bool": {
                    "filter": [
                        {"term": {f"metadata.{query.metadata_filter[i].field}.keyword": query.metadata_filter[i].value}}
                        for i in range(len(query.metadata_filter))
                    ]
                }
            }
        elif query.db_settings.provider == VectorDBProvider.PGVector:
            search_kwargs["filter"] = {filter.field: filter.value for filter in query.metadata_filter}
        else:
            raise HTTPException(
                status_code=422,
                detail=f"Unsupported vector store provider : {query.db_settings.provider}.",
            )

    return search_kwargs
