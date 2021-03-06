import click
from flask import Blueprint

from elephantcallscounter.adapters.shared.audio_events_queue import AudioEventsQueue
from elephantcallscounter.adapters.azure_interface import AzureInterface
from elephantcallscounter.services.data_processing_service import create_file_segments
from elephantcallscounter.data_processing.model_preprocessing import ModelPreprocessing
from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths
from elephantcallscounter.application.persistence.models.elephants import delete_all_elephants


data_processing = Blueprint('data_processing', __name__)


@data_processing.cli.command('generate_file_segments')
@click.argument('file_name')
@click.pass_context
def generate_file_segments(context, file_name):
    """ Command to generate the file segments from the original video.

    :return void:
    """
    create_file_segments(file_name)


@data_processing.cli.command('generate_training_data')
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


@data_processing.cli.command('cleanup_data')
def cleanup_data():
    """ Command to clean up all the data in the models.

    :return void:
    """
    delete_all_elephants()


@data_processing.cli.command('delete_queue')
@click.argument('queue_name')
def delete_queue(queue_name):
    """ Command to clean up all data in queue.

    :return void:
    """
    azure_events_queue = AudioEventsQueue(queue_name)
    azure_events_queue.delete_queue()


@data_processing.cli.command('delete_blob')
@click.argument('container_name')
@click.argument('blob_name')
def delete_blob(container_name, blob_name):
    """ Command to delete the data in a blob.

    :param string container_name:
    :param string blob_name:
    :return:
    """
    azure_interface = AzureInterface(container_name)
    azure_interface.delete_blob(blob_name)
