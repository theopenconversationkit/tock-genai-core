"""
Package pour l'orchestration d'application LLM
"""

from tock_genai_core.services.security.security_service import get_nested_value, fetch_secret_key_value

from tock_genai_core.services.langchain.factory.compressor_factory import get_compressor_factory
from tock_genai_core.services.langchain.factory.db_factory import get_vector_db_factory
from tock_genai_core.services.langchain.factory.em_factory import get_em_factory
from tock_genai_core.services.langchain.factory.factories import VectorDBFactory, LLMFactory, EMFactory, CompressorFactory, GuardrailFactory
from tock_genai_core.services.langchain.factory.guardrail_factory import get_guardrail_factory
from tock_genai_core.services.langchain.factory.llm_factory import get_llm_factory
from tock_genai_core.services.langchain.factory.contextual_compressor.bloomz_compressor_factory import BloomzCompressorFactory
from tock_genai_core.services.langchain.factory.database.opensearch_factory import OpenSearchFactory
from tock_genai_core.services.langchain.factory.database.pgvector_factory import PGVectorFactory
from tock_genai_core.services.langchain.factory.embedding.bloomz_factory import BloomzFactory
from tock_genai_core.services.langchain.factory.embedding.openai_factory import OpenAIEMFactory
from tock_genai_core.services.langchain.factory.embedding.vllm_factory import VLLMEMFactory
from tock_genai_core.services.langchain.factory.guardrail.bloomz_guardrail_factory import BloomzGuardrailFactory
from tock_genai_core.services.langchain.factory.llm.openai_factory import OpenAILLMFactory
from tock_genai_core.services.langchain.factory.llm.tgi_factory import TGIFactory
from tock_genai_core.services.langchain.factory.llm.vllm_factory import VllmFactory

from tock_genai_core.models.contextual_compressor.provider import ContextualCompressorProvider
from tock_genai_core.models.contextual_compressor.setting import BaseCompressorSetting
from tock_genai_core.models.contextual_compressor.types import CompressorSetting
from tock_genai_core.models.contextual_compressor.bloomz.bloomz_compressor_setting import BloomZCompressorSetting

from tock_genai_core.models.database.provider import VectorDBProvider
from tock_genai_core.models.database.setting import BaseVectorDBSetting
from tock_genai_core.models.database.types import DBSetting
from tock_genai_core.models.database.metadata import MetadataFilter # j'ai un doute sur celle-là
from tock_genai_core.models.database.opensearch.opensearch_db_setting import OpenSearchSetting
from tock_genai_core.models.database.pgvector.pgvector_db_setting import PGVectorSetting

from tock_genai_core.models.embedding.provider import EMProvider
from tock_genai_core.models.embedding.setting import BaseEMSetting
from tock_genai_core.models.embedding.types import EMSetting
from tock_genai_core.models.embedding.bloomz.bloomz_em_setting import BloomZEMSetting
from tock_genai_core.models.embedding.openai.openai_em_setting import OpenAIEMSetting
from tock_genai_core.models.embedding.vllm.vllm_em_setting import VLLMEMSetting

from tock_genai_core.models.guardrail.provider import GuardrailProvider
from tock_genai_core.models.guardrail.setting import BaseGuardrailSetting
from tock_genai_core.models.guardrail.types import GuardrailSetting
from tock_genai_core.models.guardrail.bloomz.bloomz_guardrail_setting import BloomZGuardrailSetting

from tock_genai_core.models.langfuse.setting import LangfuseSetting

from tock_genai_core.models.llm.provider import LLMProvider
from tock_genai_core.models.llm.setting import BaseLLMSetting
from tock_genai_core.models.llm.types import LLMSetting
from tock_genai_core.models.llm.tgi.tgi_llm_setting import HuggingFaceTextGenInferenceLLMSetting
from tock_genai_core.models.llm.openai.openai_llm_setting import OpenAILLMSetting
from tock_genai_core.models.llm.vllm.vllm_setting import VllmSetting

from tock_genai_core.models.security.secret_key import BaseSecretKey
from tock_genai_core.models.security.secret_key_type import SecretKeyType
from tock_genai_core.models.security.security_type import SecretKey
from tock_genai_core.models.security.aws_secret_key.aws_secret_key import AwsSecretKey
from tock_genai_core.models.security.kube_secret_key.kube_secret_key import KubernetesSecretKey
from tock_genai_core.models.security.raw_secret_key.raw_secret_key import RawSecretKey


__all__ = [
    "get_nested_value",
    "fetch_secret_key_value",
    "get_compressor_factory",
    "get_vector_db_factory",
    "get_em_factory",
    "VectorDBFactory",
    "LLMFactory",
    "EMFactory",
    "CompressorFactory",
    "GuardrailFactory",
    "get_guardrail_factory",
    "get_llm_factory",
    "BloomzCompressorFactory",
    "OpenSearchFactory",
    "PGVectorFactory",
    "BloomzFactory",
    "OpenAIEMFactory",
    "VLLMEMFactory",
    "BloomzGuardrailFactory",
    "OpenAILLMFactory",
    "TGIFactory",
    "VllmFactory",
    "ContextualCompressorProvider",
    "BaseCompressorSetting",
    "CompressorSetting",
    "BloomZCompressorSetting",
    "VectorDBProvider",
    "BaseVectorDBSetting",
    "DBSetting",
    "MetadataFilter",
    "OpenSearchSetting",
    "PGVectorSetting",
    "EMProvider",
    "BaseEMSetting",
    "EMSetting",
    "BloomZEMSetting",
    "OpenAIEMSetting",
    "VLLMEMSetting",
    "GuardrailProvider",
    "BaseGuardrailSetting",
    "GuardrailSetting",
    "BloomZGuardrailSetting",
    "LangfuseSetting",
    "LLMProvider",
    "BaseLLMSetting",
    "LLMSetting",
    "HuggingFaceTextGenInferenceLLMSetting",
    "OpenAILLMSetting",
    "VllmSetting",
    "BaseSecretKey",
    "SecretKeyType",
    "SecretKey",
    "AwsSecretKey",
    "KubernetesSecretKey",
    "RawSecretKey",
]

__version__ = '0.1.0'

# créer 2-3 test factory
