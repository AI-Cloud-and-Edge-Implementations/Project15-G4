from elephantcallscounter.management.commands.command_groups import entry_point
from elephantcallscounter.services.data_import import import_data_from_s3_using_boto
from elephantcallscounter.services.data_import import copy_data_to_azure_fast
from elephantcallscounter.services.data_import import download_data_from_azure_fast


@entry_point.command('import_data_from_s3')
@entry_point.pass_context
def import_data_from_s3(context):
    """ Command to read data from s3.

    :return void:
    """
    import_data_from_s3_using_boto()


@entry_point.command('copy_data_to_azure')
@entry_point.pass_context
def copy_data_to_azure_fast(context):
    """ Command to copy data to azure using optimized copy.

    :param context:
    :return void:
    """
    copy_data_to_azure_fast()


@entry_point.command('copy_data_from_azure')
@entry_point.pass_context
def copy_data_from_azure_fast(context):
    """ Command to copy data from from azure using optimized copy.

    :param context:
    :return void:
    """
    container_name = context.obj['container_name']
    download_data_from_azure_fast(container_name)
