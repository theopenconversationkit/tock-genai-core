def assert_embedding_model_matches_existing_index(index_name: str, existing_metadata: dict, requested_model: str) -> None:
    """
    Checks if the embedding model used to create an existing index matches the requested embedding model.
    Raises a ValueError if there is a mismatch.
    Adding to an existing index: newly added chunks must use the model that was used to create the index; otherwise, s
    they end up in an incompatible vector space and search results are silently corrupted.
    Unknown identity = non-blocking (no stamp or no requested model means there is nothing to compare).
    Embedding model names are normalized by trimming whitespace and removing the :latest suffix before comparison.
    
    Parameters
    ----------
    index_name : str
        The name of the index to check.
    existing_metadata : dict
        The metadata of the existing index.
    requested_model : str
        The embedding model that was requested.

    Raises
    ------
    ValueError
        If the embedding model used to create the existing index does not match the requested embedding model.

    Returns
    ------
    None
    """

    existing_model = normalize_embedding_model(existing_metadata.get('embedding_model'))
    requested_model = normalize_embedding_model(requested_model)

    if existing_model and requested_model and existing_model != requested_model:
        raise ValueError(
            f"Embedding model mismatch on existing index '{index_name}': "
            f"the index was created with '{existing_model}', "
            f"but the configuration requests '{requested_model}'."
        )


def normalize_embedding_model(model: str | None) -> str | None:
    """
    Normalizes an embedding model name by trimming whitespace and removing the :latest suffix.
    
    Parameters
    ----------
    model : str | None
        The embedding model name to normalize.

    Returns
    ------
    str | None
        The normalized embedding model name, or None if the input is None or empty.
    """
    if not model:
        return None

    model = model.strip()

    if model.endswith(":latest"):
        model = model[:-len(":latest")]

    return model or None
    