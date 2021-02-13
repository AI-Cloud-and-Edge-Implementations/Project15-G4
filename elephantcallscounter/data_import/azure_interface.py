import os
from azure.storage.blob import BlobServiceClient

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

