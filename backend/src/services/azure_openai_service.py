"""
Azure OpenAI Service

Provides integration with Azure OpenAI for chat completions and embeddings.
Uses the official openai Python library with Azure OpenAI configuration.
"""

import logging
from typing import Optional

from openai import AsyncAzureOpenAI

from config.settings import Settings

logger = logging.getLogger(__name__)


class AzureOpenAIService:
    """
    Service class for interacting with Azure OpenAI.

    Handles chat completions and embeddings using Azure OpenAI endpoints.
    Follows the service layer pattern for clean architecture.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._client: Optional[AsyncAzureOpenAI] = None

    async def initialize(self) -> None:
        """Initialize the Azure OpenAI client asynchronously."""
        if self._client is not None:
            return

        logger.info(
            "Initializing Azure OpenAI client for deployment: %s",
            self.settings.azure_openai_deployment_name,
        )

        self._client = AsyncAzureOpenAI(
            api_key=self.settings.azure_openai_api_key.get_secret_value(),
            api_version=self.settings.azure_openai_api_version,
            azure_endpoint=self.settings.azure_openai_endpoint,
            azure_deployment=self.settings.azure_openai_deployment_name,
        )

        logger.info("Azure OpenAI client initialized successfully")

    async def get_chat_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: float = 1.0,
    ) -> str:
        """
        Get a chat completion from Azure OpenAI.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys.
            temperature: Sampling temperature (0.0 to 1.0).
            max_tokens: Maximum tokens in the response.
            top_p: Nucleus sampling parameter.

        Returns:
            The response content as a string.

        Raises:
            RuntimeError: If the client is not initialized.
            openai.APIError: If the API call fails.
        """
        if self._client is None:
            raise RuntimeError(
                "Azure OpenAI client is not initialized. Call initialize() first."
            )

        kwargs = {
            "model": self.settings.azure_openai_deployment_name,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
        }

        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens

        logger.debug(
            "Sending chat completion request for deployment: %s",
            self.settings.azure_openai_deployment_name,
        )

        response = await self._client.chat.completions.create(**kwargs)

        content: str = response.choices[0].message.content or ""
        logger.debug(
            "Received chat completion response (%d tokens)",
            response.usage.total_tokens if response.usage else 0,
        )

        return content

    async def get_embeddings(
        self,
        texts: list[str],
        model: Optional[str] = None,
    ) -> list[list[float]]:
        """
        Get embeddings for a list of texts from Azure OpenAI.

        Args:
            texts: List of text strings to embed.
            model: The embedding model deployment name. Defaults to the
                   configured embedding deployment name.

        Returns:
            List of embedding vectors.

        Raises:
            RuntimeError: If the client is not initialized.
            openai.APIError: If the API call fails.
        """
        if self._client is None:
            raise RuntimeError(
                "Azure OpenAI client is not initialized. Call initialize() first."
            )

        embedding_model = model or self.settings.azure_openai_embedding_deployment_name

        logger.debug(
            "Sending embedding request for deployment: %s (texts count: %d)",
            embedding_model,
            len(texts),
        )

        response = await self._client.embeddings.create(
            model=embedding_model,
            input=texts,
        )

        embeddings: list[list[float]] = [item.embedding for item in response.data]
        logger.debug(
            "Received embeddings for %d texts (dimension: %d)",
            len(embeddings),
            len(embeddings[0]) if embeddings else 0,
        )

        return embeddings

    async def close(self) -> None:
        """Close the Azure OpenAI client and release resources."""
        if self._client is not None:
            await self._client.close()
            self._client = None
            logger.info("Azure OpenAI client closed")