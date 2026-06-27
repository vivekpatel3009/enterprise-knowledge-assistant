from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    app_name: str = Field("Enterprise Knowledge Assistant", env="APP_NAME")

    # Azure OpenAI Configuration
    azure_openai_api_key: SecretStr = Field(
        "",
        env="AZURE_OPENAI_API_KEY"
    )

    azure_openai_endpoint: str = Field(
        "",
        env="AZURE_OPENAI_ENDPOINT"
    )
    azure_storage_connection_string: str = Field(
        "",
        env="AZURE_STORAGE_CONNECTION_STRING"
    )
    azure_openai_api_version: str = Field("2024-10-21", env="AZURE_OPENAI_API_VERSION")
    azure_openai_deployment_name: str = Field(
        "gpt-4o", env="AZURE_OPENAI_DEPLOYMENT_NAME"
    )
    azure_openai_embedding_deployment_name: str = Field(
        "text-embedding-3-small", env="AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"
    )
    database_url: str = Field("sqlite:///./data/app.db", env="DATABASE_URL")
    chroma_directory: str = Field("./data/chroma", env="CHROMA_DIRECTORY")
    env_file: str = Field(".env", env="ENV_FILE")
    azure_storage_container: str = Field("documents", env="AZURE_STORAGE_CONTAINER")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()