import click

from elephantcallscounter.services.data_processing_service import create_file_segments
from elephantcallscounter.data_processing.model_preprocessing import ModelPreprocessing
from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths


@click.group('data_processing')
@click.pass_context
def data_processing(context):
    pass


@data_processing.command('generate_file_segments')
@click.argument('file_name')
@click.pass_context
def generate_file_segments(context, file_name):
    """ Command to generate the file segments from the original video.

    :return void:
    """
    create_file_segments(file_name)


@data_processing.command('generate_training_data')
@click.argument('input_folder')
@click.argument('output_folder', default=join_paths([get_project_root(), 'data/training_data']))
@click.pass_context
def generate_training_data(context, input_folder, output_folder):
    """ Command to generate the training data based of an input folder.

    :param context:
    :param string input_folder:
    :param string output_folder:
    :return void:
    """
    model_preprocessing = ModelPreprocessing(input_folder, output_folder)
    model_preprocessing.split_images_into_right_format()
