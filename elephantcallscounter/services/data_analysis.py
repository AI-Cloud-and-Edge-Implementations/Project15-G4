import os

from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.data_analysis.analyse_sound_data import AnalyseSoundData


def analyse_sound_data(file_path, dest_path):
    """ Analyse the sound data and generate spectrograms.

    :param str file_path:
    :param str dest_path:
    :return void:
    """
    sound_data_analyser = AnalyseSoundData(
        file_read_location = os.path.join(
            get_project_root(), file_path
        ),
        save_image_location = os.path.join(
            get_project_root(), dest_path
        ),
        sr = 1000,
        hop_length = 256
    )
    sound_data_analyser.analyse_audio()
