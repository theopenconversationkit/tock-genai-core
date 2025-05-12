from abc import ABC, abstractmethod

from pydantic import BaseModel
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.vectorstores import VectorStore
from langchain.base_language import BaseLanguageModel
from langchain.embeddings.base import Embeddings
from langchain.retrievers.document_compressors.base import BaseDocumentCompressor

from tock_genai_core.models.embedding import BaseEMSetting
from tock_genai_core.models.llm.setting import BaseLLMSetting
from tock_genai_core.models.database import BaseVectorDBSetting
from tock_genai_core.models.guardrail import BaseGuardrailSetting
from tock_genai_core.models.contextual_compressor import BaseCompressorSetting


class VectorDBFactory(ABC, BaseModel):
    """
    Abstract factory class for creating vector database instances.

    Attributes
    ----------
    db_settings : BaseVectorDBSetting
        The settings used to configure the vector database.

    em_settings : BaseEMSetting
        The settings used for configuring the embedding model.

    Methods
    -------
    get_vector_store() -> VectorStore
        Abstract method to be implemented by subclasses to return an instance of a vector store.
    """

    db_settings: BaseVectorDBSetting
    em_settings: BaseEMSetting

    @abstractmethod
    def get_vector_store(self) -> VectorStore:
        pass


class LLMFactory(ABC, BaseModel):
    """
    Abstract factory class for creating large language model (LLM) instances.

    Attributes
    ----------
    settings : BaseLLMSetting
        The settings used to configure the large language model.

    Methods
    -------
    get_model() -> BaseLanguageModel
        Abstract method to be implemented by subclasses to return an instance of a language model.
    """

    settings: BaseLLMSetting

    @abstractmethod
    def get_model(self) -> BaseLanguageModel:
        pass


class EMFactory(ABC, BaseModel):
    """
    Abstract factory class for creating embedding model instances.

    Attributes
    ----------
    settings : BaseEMSetting
        The settings used to configure the embedding model.

    Methods
    -------
    get_model() -> Embeddings
        Abstract method to be implemented by subclasses to return an instance of an embedding model.
    """

    settings: BaseEMSetting

    @abstractmethod
    def get_model(self) -> Embeddings:
        pass


class CompressorFactory(ABC, BaseModel):
    """
    Abstract factory class for creating document compressor instances (used for reranking).

    Attributes
    ----------
    settings : BaseCompressorSetting
        The settings used to configure the document compressor.

    Methods
    -------
    get_compressor() -> BaseDocumentCompressor
        Abstract method to be implemented by subclasses to return an instance of a document compressor.
    """

    settings: BaseCompressorSetting

    @abstractmethod
    def get_compressor(self) -> BaseDocumentCompressor:
        pass


class GuardrailFactory(ABC, BaseModel):
    """
    Abstract factory class for creating guardrail output parser instances.

    Attributes
    ----------
    settings : BaseGuardrailSetting
        The settings used to configure the guardrail output parser.

    Methods
    -------
    get_parser() -> BaseOutputParser
        Abstract method to be implemented by subclasses to return an instance of an output parser.
    """

    settings: BaseGuardrailSetting

    @abstractmethod
    def get_parser(self) -> BaseOutputParser:
        pass
