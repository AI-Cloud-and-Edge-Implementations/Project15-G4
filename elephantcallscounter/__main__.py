#!/usr/bin/env python
import os

import click

from elephantcallscounter.data_analysis.analyse_sound_data import AnalyseSoundData
from elephantcallscounter.data_processing.segment_files import FileSegmenter
from elephantcallscounter.data_import.amazon_interface import AmazonInterface


@click.group()
def entry_point():
    pass


@entry_point.command('analyse_audio_data')
def analyse_audio_data():
    analyse_sound_data = AnalyseSoundData(
        file_read_location=os.path.join(
            os.getcwd(), 'data/metadata/nn01a_20180126_000000_cropped.wav'
        ),
        save_image_location=os.path.join(
            os.getcwd(), 'data/spectrogram_images/'
        ),
        sr=1000,
        hop_length=256
    )
    analyse_sound_data.analyse_audio()


@entry_point.command('generate_file_segments')
def generate_file_segments():
    FileSegmenter.segment_files()
    # ready_file_segments()


@entry_point.command('import_data_from_s3')
def import_data_from_s3():
    amazon = AmazonInterface()
    amazon.download_all_files()


if __name__ == "__main__":
    entry_point.add_command(analyse_audio_data)
    entry_point.add_command(generate_file_segments)
    entry_point()
