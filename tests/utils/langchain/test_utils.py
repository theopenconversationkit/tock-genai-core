from tock_genai_core.utils.langchain.utils import (
    assert_embedding_model_matches_existing_index,
    normalize_embedding_model,
)


def test_assert_embedding_model_matches_existing_index():
    # Test case where existing model matches requested model
    assert_embedding_model_matches_existing_index("test_index", {"embedding_model": "model_name"}, "model_name")

    # Test case where existing model does not match requested model
    try:
        assert_embedding_model_matches_existing_index(
            "test_index", {"embedding_model": "model_name"}, "different_model"
        )
    except ValueError as e:
        assert (
            str(e)
            == "Embedding model mismatch on existing index 'test_index': the index was created with 'model_name', but the configuration requests 'different_model'."
        )

    # Test case where existing model is None
    assert_embedding_model_matches_existing_index("test_index", {}, "model_name")

    # Test case where requested model is None
    assert_embedding_model_matches_existing_index("test_index", {"embedding_model": "model_name"}, None)

    # Test case where both models are None
    assert_embedding_model_matches_existing_index("test_index", {}, None)


def test_normalize_embedding_model():

    assert normalize_embedding_model(" model_name:latest ") == "model_name"
    assert normalize_embedding_model(" model_name ") == "model_name"
    assert normalize_embedding_model("model_name:latest") == "model_name"
    assert normalize_embedding_model("model_name") == "model_name"
    assert normalize_embedding_model("") is None
    assert normalize_embedding_model(None) is None
