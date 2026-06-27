from openai import AzureOpenAI

from src.config.settings import settings


class EmbeddingService:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=settings.azure_openai_api_key.get_secret_value(),
            api_version=settings.azure_openai_api_version,
            azure_endpoint=settings.azure_openai_endpoint
        )

    def generate_embedding(
        self,
        text: str
    ) -> list[float]:

        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        try:
            response = self.client.embeddings.create(
                model=settings.azure_openai_embedding_deployment_name,
                input=text
            )
            return response.data[0].embedding

        except Exception as ex:
            raise RuntimeError(
                f"Failed to generate embedding: {str(ex)}"
            ) from ex