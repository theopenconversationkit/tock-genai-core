from langchain_openai import AzureOpenAIEmbeddings
from langchain.embeddings.base import Embeddings

from tock_genai_core.services.langchain.factory.factories import EMFactory
from tock_genai_core.models.embedding.vllm.vllm_em_setting import VLLMEMSetting
from tock_genai_core.services.security.security_service import fetch_secret_key_value


class VLLMEMFactory(EMFactory):
    settings: VLLMEMSetting

    def get_model(self) -> Embeddings:
        return AzureOpenAIEmbeddings(
            model=self.settings.model,
            azure_endpoint=self.settings.api_base,
            openai_api_key=fetch_secret_key_value(self.settings.api_key) if self.settings.api_key else "EMPTY",
        )
