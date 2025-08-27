# tock-genai-core
Composants principaux d'IA générative : models, factories, gestion des erreurs utilisés dans les composants Gen AI python de tock.

## Architecture

Le projet est structuré en trois composants principaux :

- **Models** : Contient les définitions des classes et modèles de données utilisés dans l'application
- **Services/Factories** : Regroupe la logique métier et les fonctions utilisées par les routes


## Technologies

- **Backend** : Python
- **Base de données** :
  - pgvector pour la base de données vectorielle
- **LLM & RAG** :
  - Langchain pour l'orchestration
  - Support de guardrails
  - Reranker pour l'amélioration des résultats
  - Langfuse pour le monitoring


## Providers disponibles

- **LLMProvider** (LLM)
    - TGI = "HuggingFaceTextGenInference"
    - OpenAI = "OpenAI"
    - Vllm = "Vllm"

- **GuardrailProvider** (Guardrail)
    - BloomZ = "BloomzGuardrail"

- **EMProvider** (Embedding)
    - BloomZ = "BloomzEmbeddings"
    - OpenAI = "OpenAI"
    - Vllm = "Vllm"

- **VectorDBProvider** (Database)
    - OpenSearch = "OPENSEARCH"
    - PGVector = "PGVECTOR"

- **ContextualCompressorProvider** (Contetual Compressor)
    - BloomZ = "BloomzRerank"

## Secret Keys

Types disponibles :  
- **RawSecretKey** : stocke directement la valeur du secret.  
  - Champ principal : `secret`  
  - Alias rétro-compatible : `value` (encore utilisable pour compatibilité, mais à éviter dans les nouvelles configurations).
- **AwsSecretKey** : référence un secret dans **AWS Secrets Manager**.  
- **KubernetesSecretKey** : référence un secret dans **Kubernetes Secrets**.  
- **GcpSecretKey** : référence un secret dans **GCP Secret Manager**.

### GCP Secret Manager

Pour utiliser `GcpSecretKey`, un `project_id` GCP doit être disponible.  
Il est résolu automatiquement de la façon suivante :

1. Si la variable d’environnement `GCP_PROJECT_ID` est définie -> elle est utilisée directement.  
2. Sinon, le `project_id` est automatiquement détecté à partir des credentials Google (`GOOGLE_APPLICATION_CREDENTIALS`).  

## Settings

- **Embedding**
  
  - Classe parente
    ```
    BaseEMSetting:
        provider: EMProvider
        model: Optional[str]
        api_key: Optional[SecretKey]
        api_base: str
        pooling: Optional[str]
        space_type: Optional[str]
    ```
  - Classes enfants
    ```
    BloomZEMSetting(BaseEMSetting):
        provider: Literal[EMProvider.BloomZ]
    ```


    ```
    VLLMEMSetting(BaseEMSetting):
        provider: Literal[EMProvider.Vllm]
        model: str
    ```


    ```
    OpenAIEMSetting(BaseEMSetting):
        provider: Literal[EMProvider.OpenAI]
        api_base: str
        api_version: str
        deployment: str
    ```

- **Contextual compressor**

  - Classe parente
    ```
    BaseCompressorSetting:
        provider: ContextualCompressorProvider
        endpoint: str
        api_key: Optional[SecretKey]
    ```

  - Classe enfant
    ```
    BloomZCompressorSetting(BaseCompressorSetting):
        provider: Literal[ContextualCompressorProvider.BloomZ]
        min_score: float
        max_documents: Optional[int]
        label: Optional[str]
    ```

- **Database** 

  - Classe parente
    ```
    BaseVectorDBSetting:
        index: Optional[str]
        provider: VectorDBProvider
        db_url: str
    ```
  - Classes enfants
    ```
    OpenSearchSetting(BaseVectorDBSetting):
        provider: Literal[VectorDBProvider.OpenSearch]
        username: SecretKey
        password: SecretKey
        use_ssl: bool
        verify_certs: bool
    ```

    ```
    class PGVectorSetting(BaseVectorDBSetting):
        provider: Literal[VectorDBProvider.PGVector]
        username: SecretKey
        password: SecretKey 
        db_name: str
        sslmode: Optional[str]
        namespace: str
    ```

- **Guardrail**

  - Classe parente
    ```
    BaseGuardrailSetting:
        provider: GuardrailProvider
        api_base: str
        max_score: Optional[float]
        api_key: Optional[SecretKey]
    ```

  - Classe enfant
    ```
    BloomZGuardrailSetting(BaseGuardrailSetting):
        provider: Literal[GuardrailProvider.BloomZ]
    ```

- **Langfuse**
  ```
  LangfuseSetting:
      host: Optional[str]
      public_key: Optional[SecretKey]
      secret_key: Optional[SecretKey]
      metadata: Optional[Dict[str, Any]]
  ```

- **LLM**

  - Classe parente
    ```
    BaseLLMSetting:
        provider: LLMProvider
        model: Optional[str]
        api_key: Optional[SecretKey]
        temperature: float
    ```

  - Classes enfants
    ```
    OpenAILLMSetting(BaseLLMSetting):
        provider: Literal[LLMProvider.OpenAI]
        api_base: str
        api_version: str
        deployment: str
    ```

    ```
    HuggingFaceTextGenInferenceLLMSetting(BaseLLMSetting):
        provider: Literal[LLMProvider.TGI]
        repetition_penalty: float
        max_new_tokens: int
        api_base: str
        streaming: bool
    ```

    ```
    VllmSetting(BaseLLMSetting):
        provider: Literal[LLMProvider.Vllm]
        api_base: str
        max_new_tokens: int
        additional_model_kwargs: Optional[Dict[str, Any]]
    ```

## Fonctionnement

Chaque outil utilisé (database, embedding, llm, langfuse, ...) a besoin d'un certains nombre de paramètres qui sont référencés dans les models (classes de settings)

Ces classes sont ensuite héritées par des services ou des factories afin de pouvoir répondre au besoin.


Exemple de `get_vector_db_factory` qui crée une factory de base vectorielle basée sur le nom de l'application et les paramètres d'embedding fournis

```python
from tock-genai-core import get_vector_db_factory
from tock-genai-core import PGVectorSetting, VLLMEMSetting
from tock-genai-core import DBSetting, EMSetting


db_settings = PGVectorSetting(
    index = "first_index",
    provider = "PGVECTOR",
    db_url = "127.0.0.1:XXXX",
    db_name = "rag_sandbox_db",
    sslmode = "disable",
    username = {
      type = "Raw",
      value = "admin"
    },
    password = {
      type = "Raw",
      value = "example"
    },
    namespace = "test-name"
)

em_settings = VLLMEMSetting(
    provider = "Vllm",
    model = "model_name",
    api_base = "https://continue.com/v1"
)



def function_name(db_settings: DBSetting, em_settings: EMSetting):

    # do somethings

    vector = get_vector_db_factory(db_settings: DBSetting, em_settings: BaseEMSetting)

    # do somethings
```
