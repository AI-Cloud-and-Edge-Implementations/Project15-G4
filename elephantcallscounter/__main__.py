#!/usr/bin/env python
import os

import click

from elephantcallscounter.data_import.amazon_interface import AmazonInterface
from elephantcallscounter.data_import.az_copy import AzureDataImporter
from elephantcallscounter.data_analysis.analyse_sound_data import AnalyseSoundData
from elephantcallscounter.data_processing.segment_files import SegmentFiles
from elephantcallscounter.utils.path_utils import get_project_root


@click.group()
def entry_point():
    pass


@entry_point.command('analyse_audio_data')
def analyse_audio_data():
    """ Command to analyse the audio data and generate neccesary plots.

    :return void:
    """
    analyse_sound_data = AnalyseSoundData(
        file_read_location = os.path.join(
            os.getcwd(), 'data/metadata/nn01a_20180126_000000_cropped.wav'
        ),
        save_image_location = os.path.join(
            os.getcwd(), 'data/spectrogram_images/'
        ),
        sr = 1000,
        hop_length = 256
    )
    analyse_sound_data.analyse_audio()


@entry_point.command('generate_file_segments')
def generate_file_segments():
    """ Command to generate the file segments from the original video.

    :return void:
    """
    az_data_importer = AzureDataImporter(
        source_directory=os.path.join(get_project_root(), 'data', 'rumble_landscape_general'),
        blob_string = "project15team4.blob.core.windows.net",
        container_name = "elephant-sound-data"
    )
    segment_files = SegmentFiles(az_data_importer, True)
    segment_files.process_segments(segment_files.ready_file_segments())


@entry_point.command('import_data_from_s3')
def import_data_from_s3():
    """ Command to read data from s3.

    :return void:
    """
    amazon_interface = AmazonInterface()
    files = amazon_interface.read_from_s3()


@entry_point.command('copy_data_to_azure')
def copy_data_to_azure():
    """ Command to copy data to azure using optimized azcopy.

    :return void:
    """
    az_data_importer = AzureDataImporter(
        source_directory=os.path.join(get_project_root(), 'data', 'rumble_landscape_general'),
        blob_string = "project15team4.blob.core.windows.net",
        container_name = "elephant-sound-data"
    )
    az_data_importer.send_to_copy_handler()


if __name__ == "__main__":
    entry_point()
