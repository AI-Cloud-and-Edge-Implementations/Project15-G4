import click
from flask import Blueprint

from elephantcallscounter.adapters.azure_interface import AzureInterface
from elephantcallscounter.services.data_import_service import (
    import_data_from_s3_using_boto,
)
from elephantcallscounter.services.data_import_service import copy_file_to_azure_fast
from elephantcallscounter.services.data_import_service import (
    download_data_from_azure_fast,
)

data_import = Blueprint("data_import", __name__)


@data_import.cli.command("import_data_from_s3")
@click.pass_context
def import_data_from_s3(context):
    """Command to read data from s3.

    :param context:
    :return void:
    """
    import_data_from_s3_using_boto()


@data_import.cli.command("copy_blob_from_azure")
@click.argument("container_name")
@click.argument("source_folder")
@click.argument("destination_folder")
@click.pass_context
def download_from_azure(context, container_name, source_folder, destination_folder):
    """Command to copy data from from azure using blob storage.

    :param context:
    :param string container_name:
    :param string source_folder:
    :param string destination_folder:
    :return void:
    """
    azure_interface = AzureInterface(container_name=container_name)
    azure_interface.download_from_azure(source_folder, destination_folder)


@data_import.cli.command("copy_data_to_azure")
@click.argument("container_name")
@click.argument("source_file")
@click.argument("destination_folder")
@click.pass_context
def copy_data_to_azure_fast(context, container_name, source_file, destination_folder):
    """Command to copy data to azure using optimized copy.

    :param context:
    :param string container_name:
    :param string source_file:
    :param string destination_folder:
    :return void:
    """
    copy_file_to_azure_fast(container_name, source_file, destination_folder)


@data_import.cli.command("copy_data_from_azure")
@click.argument("container_name")
@click.argument("source_file")
@click.argument("destination_file")
@click.pass_context
def copy_data_from_azure_fast(context, container_name, source_file, destination_file):
    """Command to copy data from from azure using optimized copy.

    :param context:
    :param string container_name:
    :param string source_file:
    :param string destination_file:
    :return void:
    """
    download_data_from_azure_fast(container_name, source_file, destination_file)
