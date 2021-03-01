import click

from elephantcallscounter.services.data_processing_service import create_file_segments


@click.group('data_processing')
@click.pass_context
def data_processing(context):
    pass


@data_processing.command('generate_file_segments')
@click.pass_context
@click.argument('file_name')
def generate_file_segments(context, file_name):
    """ Command to generate the file segments from the original video.

    :return void:
    """
    create_file_segments(file_name)
