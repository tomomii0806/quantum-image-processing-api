from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

class AzureBlobService:
    def __init__(self):
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME")
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

    def get_image(self, image_id: str):
        blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=image_id)
        try:
            blob_data = blob_client.download_blob()
            return blob_data.readall()
        except Exception as e:
            return {"error": str(e)}