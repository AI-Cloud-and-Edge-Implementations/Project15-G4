import click
from flask import Blueprint
import os

from elephantcallscounter.services.data_analysis_service import analyse_sound_data
from elephantcallscounter.services.data_analysis_service import create_mono_spectrograms
from elephantcallscounter.services.data_analysis_service import find_elephants_in_images
from elephantcallscounter.services.data_analysis_service import run_cnn
from elephantcallscounter.utils.path_utils import join_paths
from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import split_file_path

data_analysis = Blueprint('data_analysis', __name__)


@data_analysis.cli.command('generate_spectrograms')
@click.argument('source_path')
@click.argument('dest_path')
@click.pass_context
def generate_spectrograms(context, source_path, dest_path):
    """ Command to analyse the audio data and generate necessary spectrogram.

    :return void:
    """
    if os.path.isfile(source_path):
        analyse_sound_data(source_path, dest_path)
    elif os.path.isdir(source_path):
        for file in os.listdir(source_path):
            dir_path = split_file_path(source_path, "/", 2)[-1]
            analyse_sound_data(
                os.path.join(source_path, file),
                os.path.join(dest_path, dir_path)
            )


@data_analysis.cli.command('generate_multiple_spectrograms')
@click.argument('source_path')
@click.argument('dest_path')
@click.pass_context
def analyse_multiple_audio_files(context, source_path, dest_path):
    """ Command to analyse multiple audio files in directory and generate spectrogram.

    :param context:
    :param string source_path:
    :param string dest_path:
    :return void:
    """
    context.obj['dest_path'] = dest_path
    for file in os.listdir(source_path):
        file_path = os.path.join(file)
        context.invoke(
            generate_spectrograms,
            source_path = os.path.join(source_path, file_path),
            dest_path = dest_path
        )


@data_analysis.cli.command('monochrome')
@click.argument('source_folder')
@click.argument('target_folder')
def monochrome(source_folder, target_folder):
    create_mono_spectrograms(source_folder, target_folder)


@data_analysis.cli.command('find_elephants')
@click.argument('dir_name')
@click.argument('dest_folder')
@click.argument('csv_file_path', default = 'data/labels/spec_images_labels.csv')
@click.pass_context
def find_elephants_command(context, dir_name, dest_folder, csv_file_path):
    """ Command to analyse spectrograms and generate bounding box images of possible elephants.

    :param context:
    :param string dir_name:
    :param string dest_folder:
    :param string csv_file_path:
    :return void:
    """
    find_elephants_in_images(
        os.path.join(get_project_root(), dir_name),
        os.path.join(get_project_root(), dest_folder),
        os.path.join(get_project_root(), csv_file_path)
    )


@data_analysis.cli.command('train_cnn')
@click.argument('training_loc')
@click.argument('model_name')
def train_cnn(training_loc, model_name):
    elephant_counter_resnet = ElephantCounterResnet(
        training_loc = join_paths([get_project_root(), training_loc]),
        model_name = model_name
    )
    elephant_counter_resnet.build_model()


@data_analysis.cli.command('run_cnn')
@click.argument('model_name')
@click.argument('dir_path')
def run_cnn_command(dir_path, model_name):
    run_cnn(dir_path, model_name)
