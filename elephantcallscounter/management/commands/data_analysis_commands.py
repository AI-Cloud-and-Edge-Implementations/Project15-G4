import os

from elephantcallscounter.management.commands.command_groups import entry_point
from elephantcallscounter.services.data_analysis import analyse_sound_data


@entry_point.command('analyse_audio_data')
@entry_point.pass_context
def analyse_audio_data(context):
    """ Command to analyse the audio data and generate necessary spectrograms.

    :return void:
    """
    file_path = context.obj['path']
    analyse_sound_data(file_path)


@entry_point.command('analyse_audio_data')
@entry_point.pass_context
def analyse_multiple_audio_files(context):
    """ Command to analyse multiple audio files in directory and generate spectrograms.

    :param context:
    :return void:
    """
    dir_path = context.obj['path']
    for file in os.listdir(dir_path):
        context.invoke(analyse_audio_data, args = {'path': file})
