import click

from elephantcallscounter.services.data_import_service import import_data_from_s3_using_boto
from elephantcallscounter.services.data_import_service import copy_data_to_azure_fast
from elephantcallscounter.services.data_import_service import download_data_from_azure_fast


@click.group('data_import')
@click.pass_context
def data_import(context):
    pass


@data_import.command('import_data_from_s3')
@click.pass_context
def import_data_from_s3(context):
    """ Command to read data from s3.

    :return void:
    """
    import_data_from_s3_using_boto()


@data_import.command('copy_data_to_azure')
@click.pass_context
def copy_data_to_azure_fast(context):
    """ Command to copy data to azure using optimized copy.

    :param context:
    :return void:
    """
    copy_data_to_azure_fast()


@data_import.command('copy_data_from_azure')
@click.argument('source_file')
@click.argument('destination_file')
@click.pass_context
def copy_data_from_azure_fast(context, source_file, destination_file):
    """ Command to copy data from from azure using optimized copy.

    :param context:
    :param string source_file:
    :param string destination_file:
    :return void:
    """
    container_name = context.obj['container_name']
    download_data_from_azure_fast(container_name, source_file, destination_file)
