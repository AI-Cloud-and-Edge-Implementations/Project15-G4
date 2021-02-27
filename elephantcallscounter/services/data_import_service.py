import os

from elephantcallscounter.config import env
from elephantcallscounter.data_import.az_copy import AzureDataImporter
from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.adapters.amazon_interface import AmazonInterface


def copy_data_to_azure_fast():
    """ This is a multithreaded copy of data to azure.

    :return void:
    """
    az_data_importer = AzureDataImporter(
        source_directory=os.path.join(get_project_root(), 'data', 'rumble_landscape_general'),
        blob_string = "project15team4.blob.core.windows.net",
        container_name = "elephant-sound-data"
    )
    az_data_importer.send_to_copy_handler()


def download_data_from_azure_fast(
        container_name, source_folder, dest_folder
):
    """ This downloads all data from azure blob using azcopy.

    :param string container_name:
    :param string source_folder:
    :param string dest_folder:
    :return:
    """
    os.makedirs(dest_folder, exist_ok = True)
    print(f'Processing {source_folder}...')
    az_data_importer = AzureDataImporter(
        source_directory=os.path.join(get_project_root(), 'data', 'rumble_landscape_general'),
        blob_string = env.AZURE_STORAGE_ACCOUNT,
        container_name = container_name
    )
    p1 = az_data_importer.az_download_data_from_blob(
        source_path = source_folder,
        destination_path = dest_folder
    )
    print(f'Processing {source_folder} finished!')
    print(f'Sent file to {dest_folder}')


def import_data_from_s3_using_boto():
    """ This is a boto read from s3.

    :return:
    """
    amazon = AmazonInterface()
    amazon.download_all_files(delete_data = True, segment_files = True)
