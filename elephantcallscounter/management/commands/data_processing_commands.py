from elephantcallscounter.management.commands.command_groups import entry_point
from elephantcallscounter.services.data_processing import create_file_segments
from elephantcallscounter.services.data_processing import create_file_segments_az_data_importer


@entry_point.command('create_segments')
@entry_point.pass_context
def create_segments(context):
    create_file_segments()


@entry_point.command('generate_file_segments')
@entry_point.pass_context
def generate_file_segments(context):
    """ Command to generate the file segments from the original video.

    :return void:
    """
    create_file_segments_az_data_importer()


@entry_point.command('full_cycle')
@entry_point.pass_context
def full_cycle(context):
    """ Command to run the full cycle of the data processing.

    :return:
    """
    pass
