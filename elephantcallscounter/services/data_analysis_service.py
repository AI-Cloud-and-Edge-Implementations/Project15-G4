import os
import pandas as pd

from elephantcallscounter.data_analysis.analyse_sound_data import AnalyseSoundData
from elephantcallscounter.data_analysis.boxing import Boxing
from elephantcallscounter.data_analysis.monochrome import Monochrome
from elephantcallscounter.models.resnet_model import ElephantCounterResnet
from elephantcallscounter.utils.file_utils import get_files_in_dir
from elephantcallscounter.utils.path_utils import get_project_root


def analyse_sound_data(file_path, dest_path):
    """Analyse the sound data and generate spectrograms.

    :param str file_path:
    :param str dest_path:
    :return void:
    """
    sound_data_analyser = AnalyseSoundData(
        file_read_location=os.path.join(get_project_root(), file_path),
        save_image_location=os.path.join(get_project_root(), dest_path),
        sr=1000,
        hop_length=256,
    )
    sound_data_analyser.analyse_audio()


def find_elephants_in_images(dir_name, dest_folder, csv_file_path):
    """Analyse the spectrograms and generate the bounding box images.

    :param str dir_name:
    :param str dest_folder:
    :param str csv_file_path:
    :return:
    """
    monochrome = Monochrome(dest_folder)
    boxing = Boxing(dir_name, dest_folder, csv_file_path, monochrome, True)
    boxed_metadata = []
    for file in get_files_in_dir(dir_name):
        elephants = boxing.create_boxes(file)
        boxed_metadata.append((file, elephants))

    dataset = pd.DataFrame(boxed_metadata)
    boxing.write_labels_to_csv_file(dataset)


def box_single_file(image_filename):
    boxing = Boxing("", "", "", "", False)
    boxed_image = boxing.create_boxes(image_filename)
    return boxed_image


def create_mono_spectrograms(image_folder, target_folder, write_file=False):
    """Create the mono spectrograms.

    :param list image_folder:
    :param string target_folder:
    :param bool write_file:
    :return void:
    """
    monochrome = Monochrome(target_folder)
    for file in image_folder:
        monochrome.create_monochrome(file, write_file)


def run_cnn(model_name, dir_path):
    elephant_counter_resnet = ElephantCounterResnet(model_name)
    return elephant_counter_resnet.run_model(dir_path)
