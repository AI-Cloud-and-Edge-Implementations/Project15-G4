import click

from elephantcallscounter.services.data_import_service import import_data_from_s3_using_boto
from elephantcallscounter.services.data_import_service import copy_file_to_azure_fast
from elephantcallscounter.services.data_import_service import download_data_from_azure_fast


@click.group('data_import')
@click.pass_context
def data_import(context):
    pass


@data_import.command('import_data_from_s3')
@click.pass_context
def import_data_from_s3(context):
    """ Command to read data from s3.

    :param context:
    :return void:
    """
    import_data_from_s3_using_boto()


@data_import.command('copy_data_to_azure')
@click.argument('container_name')
@click.argument('source_file')
@click.argument('destination_folder')
@click.pass_context
def copy_data_to_azure_fast(context, container_name, source_file, destination_folder):
    """ Command to copy data to azure using optimized copy.

    :param context:
    :param string container_name:
    :param string source_file:
    :param string destination_folder:
    :return void:
    """
    copy_file_to_azure_fast(container_name, source_file, destination_folder)


@data_import.command('copy_data_from_azure')
@click.argument('container_name')
@click.argument('source_file')
@click.argument('destination_file')
@click.pass_context
def copy_data_from_azure_fast(context, container_name, source_file, destination_file):
    """ Command to copy data from from azure using optimized copy.

    :param context:
    :param string container_name:
    :param string source_file:
    :param string destination_file:
    :return void:
    """
    container_name = context.obj['container_name']
    download_data_from_azure_fast(container_name, source_file, destination_file)
