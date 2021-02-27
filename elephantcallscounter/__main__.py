#!/usr/bin/env python
import os

import click

from data_visualizations.boxing import Boxing
from data_visualizations.monochrome import Monochrome
from elephantcallscounter.data_analysis.analyse_sound_data import AnalyseSoundData
from elephantcallscounter.data_processing.segment_files import FileSegmenter
from elephantcallscounter.data_import.amazon_interface import AmazonInterface


@click.group()
def entry_point():
    pass


# 1. Import Data
@entry_point.command('import_data')
def import_data():
    import_data_from_s3()


def import_data_from_s3(delete_data: bool = False, segment_files: bool = True):
    amazon = AmazonInterface()
    amazon.download_all_files(delete_data, segment_files)


# 2. Create Segments
@entry_point.command('generate_segments')
def create_segments():
    create_file_segments()


def create_file_segments(delete_data: bool = False):
    FileSegmenter.segment_files(delete_data)


# 3. Create Spectrograms
@entry_point.command('analyse_audio_data')
def analyse_audio_data():
    create_spectrograms()


def create_spectrograms():
    for filename in os.listdir('data/segments/train'):
        print(f'Processing {filename}...')
        analyse_sound_data = AnalyseSoundData(
            file_read_location=os.path.join(
                os.getcwd(), 'data/segments/train/' + filename
            ),
            save_image_location=os.path.join(
                os.getcwd(), 'data/spectrograms/3000_100/'  # + filename
            ),
            sr=1000,
            hop_length=256
        )
        analyse_sound_data.analyse_audio()


# 4. Monochrome spectrograms
@entry_point.command('monochrome')
def monochrome():
    create_mono_spectrograms()


def create_mono_spectrograms():
    source_folder = 'data/spectrograms/train/'
    target_folder = 'data/spectrograms/mono/'

    m = Monochrome(source_folder, target_folder)
    for filename in os.listdir(source_folder):
        m.create_monochrome(filename)


# 5. boxing and counting
@entry_point.command('boxing')
def boxing():
    create_boxes()


def create_boxes():
    source_folder = 'data/spectrograms/mono/'
    target_folder = 'data/spectrograms/boxed2/'

    if not os.path.exists(target_folder):
        os.mkdir(target_folder)

    b = Boxing(source_folder, target_folder)
    for filename in os.listdir(source_folder):
        b.create_contours_and_boxes(filename)


# x. Full cycle
@entry_point.command('full_cycle')
def full_cycle():
    import_data_from_s3(True, True)
    monochrome()
    boxing()


if __name__ == "__main__":
    entry_point.add_command(import_data)
    entry_point.add_command(create_segments)
    entry_point.add_command(analyse_audio_data)
    entry_point.add_command(monochrome)
    entry_point.add_command(full_cycle)
    entry_point.add_command(boxing)
    entry_point()
