import os
from elephantcallscounter.data_analysis.analyse_sound_data import AnalyseSoundData


def analyse_sound_data(file_path):
    """ Analyse the sound data and generate spectrograms.

    :param str file_path:
    :return void:
    """
    sound_data_analyser = AnalyseSoundData(
        file_read_location = os.path.join(
            os.getcwd(), file_path
        ),
        save_image_location = os.path.join(
            os.getcwd(), file_path
        ),
        sr = 1000,
        hop_length = 256
    )
    sound_data_analyser.analyse_audio()
