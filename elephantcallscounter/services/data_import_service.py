import logging
import os

from elephantcallscounter.adapters.amazon_interface import AmazonInterface
from elephantcallscounter.config import env
from elephantcallscounter.data_import.az_copy import AzureDataImporter
from elephantcallscounter.utils.path_utils import get_project_root

logger = logging.getLogger(__name__)


def copy_data_from_s3_to_azure_fast():
    """This is a multithreaded copy of data to azure from s3.

    :return void:
    """
    az_data_importer = AzureDataImporter(
        source_directory=os.path.join(
            get_project_root(), "data", "rumble_landscape_general"
        ),
        blob_string="project15team4.blob.core.windows.net",
        container_name="elephant-sound-data",
    )
    az_data_importer.send_to_copy_handler()


def copy_file_to_azure_fast(container_name, source_file_name, dest_folder):
    """This copies data to azure blob using azcopy.

    :param string container_name:
    :param string source_file_name:
    :param string dest_folder:
    :return:
    """
    logger.info(f"Processing {source_file_name}...")
    az_data_importer = AzureDataImporter(
        source_directory=os.path.join(
            get_project_root(), "data", "rumble_landscape_general"
        ),
        blob_string=env.AZURE_STORAGE_ACCOUNT,
        container_name=container_name,
    )
    logger.info("Sending file: %s to %s", source_file_name, dest_folder)
    az_data_importer.az_upload_data_to_blob(
        source_path=source_file_name, destination_path=dest_folder
    )
    logger.info(f"Processing {source_file_name} finished!")
    logger.info(f"Sent file to {dest_folder}")


def download_data_from_azure_fast(container_name, source_folder, dest_folder):
    """This downloads all data from azure blob using azcopy.

    :param string container_name:
    :param string source_folder:
    :param string dest_folder:
    :return:
    """
    os.makedirs(dest_folder, exist_ok=True)
    logger.info(f"Processing {source_folder}...")
    az_data_importer = AzureDataImporter(
        source_directory=os.path.join(
            get_project_root(), "data", "rumble_landscape_general"
        ),
        blob_string=env.AZURE_STORAGE_ACCOUNT,
        container_name=container_name,
    )
    az_data_importer.az_download_data_from_blob(
        source_path=source_folder, destination_path=dest_folder
    )
    logger.info(f"Processing {source_folder} finished!")
    logger.info(f"Sent file to {dest_folder}")


def import_data_from_s3_using_boto():
    """This is a boto read from s3.

    :return:
    """
    amazon = AmazonInterface()
    amazon.download_all_files(delete_data=True, segment_files=True)
