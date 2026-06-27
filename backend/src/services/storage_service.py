from azure.storage.blob import BlobServiceClient
from src.config.settings import settings


class StorageService:

    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(
            settings.azure_storage_connection_string
        )

    async def upload_file(
        self,
        file_name: str,
        file_content: bytes
    ) -> str:

        blob_client = self.blob_service_client.get_blob_client(
            container=settings.azure_storage_container,
            blob=file_name
        )

        blob_client.upload_blob(
            file_content,
            overwrite=True
        )

        return blob_client.url