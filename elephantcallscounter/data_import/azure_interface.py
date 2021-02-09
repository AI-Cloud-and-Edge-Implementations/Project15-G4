import os
from azure.storage.blob import BlobServiceClient


class AzureInterface:
    def __init__(self, container_name):
        self.container_name = container_name
        self.blob_service_client = BlobServiceClient.from_connection_string(
            'DefaultEndpointsProtocol=https;AccountName=project15;AccountKey=XXX;EndpointSuffix=core.windows.net'
        )

    def create_container(self, container_name):
        container_client = self.blob_service_client.create_container(container_name)

    def connect_to_container(self, container_name):

        blob_container_client = self.blob_service_client.get_container_client(container_name)

        return blob_container_client

    def send_to_azure(self, amazon_interface, files):
        # create a container (replace account key with actual one)
        container_name = 'elephant'

        for key in files:
            path = key['Key']
            filename = path.rsplit('/', 1)[1]
            try:
                if filename.endswith('.wav'):
                    print('Downloading ' + path + '...')
                    amazon_interface.download_s3_file(path, filename)
                    # store in blob
                    print('Storing ' + filename + ' in Azure Blob...')
                    blob_client = self.blob_service_client.get_blob_client(
                        container=container_name, blob=filename
                    )
                    with open(filename, "rb") as data:
                        blob_client.upload_blob(data)
                    # delete local file
                    os.remove(filename)
                    print('Done!')
            except Exception as e:
                print('Error while downloading ' + filename + ': ' + str(e))

