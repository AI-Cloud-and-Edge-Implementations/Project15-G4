import os

from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.data_analysis.analyse_sound_data import AnalyseSoundData
from elephantcallscounter.data_analysis.image_processing import find_number_of_clusters


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


def find_elephants(dir_name, dest_folder, csv_file_path):
    """ Analyse the spectrograms and generate the bounding box images.

    :param str dir_name:
    :param str dest_folder:
    :param str csv_file_path:
    :return:
    """
    find_number_of_clusters(dir_name, dest_folder, csv_file_path)
