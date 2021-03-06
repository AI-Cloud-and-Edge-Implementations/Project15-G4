import os
import logging
import azure.core.exceptions
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobClient

from elephantcallscounter.config import env
from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths

logger = logging.getLogger(__name__)


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

    def send_to_azure(self, original_file, dir_path, filename):
        logger.info('Storing ' + filename + ' in Azure Blob...' + dir_path)
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name, blob=join_paths([dir_path, filename])
            )
            with open(original_file, "rb") as data:
                blob_client.upload_blob(data)
            # delete local file
            os.remove(original_file)
            logger.info('Done uploading file!', dir_path + filename)
        except Exception as e:
            logger.info('Error while uploading ' + filename + ': ' + str(e))

    def download_from_azure(self, source_file, dest_file):
        try:
            blob = BlobClient(
                account_url = env.AZURE_STORAGE_ACCOUNT,
                container_name = self.container_name,
                blob_name = source_file,
                credential = env.STORAGE_SAS_KEY
            )
            with open(join_paths([get_project_root(), dest_file]), "wb+") as f:
                data = blob.download_blob()
                data.readinto(f)
        except azure.core.exceptions.ResourceNotFoundError:
            logger.info('Blob not found %s', source_file)

