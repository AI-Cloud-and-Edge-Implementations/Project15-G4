import click
import os

from elephantcallscounter.services.data_analysis import analyse_sound_data
from elephantcallscounter.utils.path_utils import split_file_path


@click.group('data_analysis')
@click.pass_context
def data_analysis(context):
    pass


@data_analysis.command('generate_spectrograms')
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


@data_analysis.command('generate_multiple_spectrograms')
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
