import click

from elephantcallscounter.services.data_processing import create_file_segments


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


@data_processing.command('full_cycle')
@click.pass_context
def full_cycle(context):
    """ Command to run the full cycle of the data processing.

    :return:
    """
    pass
