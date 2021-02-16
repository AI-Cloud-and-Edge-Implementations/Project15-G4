import os
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobClient

from elephantcallscounter.config import env


class AzureInterface:
    def __init__(self, container_name):
        self.container_name = container_name
        self.blob_service_client = BlobServiceClient.from_connection_string(
            env.CONNECTION_STRING
        )

    def create_container(self, container_name):
        self.blob_service_client.create_container(container_name)

    def connect_to_container(self, container_name):

        blob_container_client = self.blob_service_client.get_container_client(container_name)

        return blob_container_client

    def send_to_azure(self, files):
        for key in files:
            path = key['Key']
            filename = path.rsplit('/', 1)[1]
            try:
                print('Storing ' + filename + ' in Azure Blob...')
                blob_client = self.blob_service_client.get_blob_client(
                    container=self.container_name, blob=filename
                )
                with open(filename, "rb") as data:
                    blob_client.upload_blob(data)
                # delete local file
                os.remove(filename)
                print('Done!')
            except Exception as e:
                print('Error while downloading ' + filename + ': ' + str(e))

    def download_from_azure(self, source_file, dest_file):
        blob = BlobClient(account_url = env.AZURE_STORAGE_ACCOUNT,
                          container_name = self.container_name,
                          blob_name = source_file,
                          credential = env.STORAGE_SAS_KEY)

        with open(os.path.join(dest_file), "wb") as f:
            data = blob.download_blob()
            data.readinto(f)
