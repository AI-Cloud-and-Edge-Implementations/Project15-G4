import os
import pandas as pd
from pydub import AudioSegment

from data_analysis.analyse_sound_data import AnalyseSoundData


class FileSegmenter:
    def __init__(self):
        pass

    @staticmethod
    def segment_files(delete_data: bool = False):
        # read metadata
        train_or_test = 'test'

        if train_or_test == 'train':
            metadata_filepath = 'data/metadata/nn_ele_hb_00-24hr_TrainingSet_v2.txt'  # train
        else:
            metadata_filepath = 'data/metadata/nn_ele_00-24hr_GeneralTest_v4.txt'  # test
        metadata = pd.read_csv(metadata_filepath, sep='\t', header=0)
        print(f'Using metadata file {metadata_filepath}')

        slack_time = 5000  # the amount of milliseconds before and after each interesting segment

        # process raw files
        for filename in os.listdir('data/raw'):
            FileSegmenter.segment_file(filename, metadata, slack_time, train_or_test, delete_data)

    @staticmethod
    def segment_file(filename, metadata, slack_time, train_or_test, delete_data: bool = False, create_spectrograms: bool = False):
        print(f'Processing {filename}...')
        file = AudioSegment.from_wav('data/raw/' + filename)
        print(f'Processing file data/raw/{filename}...')
        # get the relevant segments from the metadata
        metadata_segments = metadata[metadata['filename'] == filename]
        for index, metadata_segment in metadata_segments.iterrows():
            try:
                selection = metadata_segment["Selection"]
                print(f' Generating segment {selection}...')

                marginal = str(metadata_segment['marginals']).strip()
                segment_path = f'data/segments/{train_or_test}/{filename}_segment_{selection}_{marginal}.wav'

                if os.path.exists(segment_path):
                    print(f'Segment file {segment_path} already exists, skipping...')
                else:
                    start = (metadata_segment['File Offset (s)'] * 1000) - slack_time  # ms
                    duration = (metadata_segment['duration'] * 1000) + (slack_time * 2)  # ms
                    end = start + duration
                    segment = file[start:end]
                    segment.export(segment_path, format='wav')
                    print(f' Found segment of {segment.duration_seconds} seconds, exported to {segment_path}.')

                # spectrograms
                if create_spectrograms:
                    analyse_sound_data = AnalyseSoundData(
                        file_read_location=os.path.join(
                            os.getcwd(), segment_path  # f'data/segments/{train_or_test}/' + filename
                        ),
                        save_image_location=os.path.join(
                            os.getcwd(), f'data/spectrograms/{train_or_test}/'  # + filename
                        ),
                        sr=1000,
                        hop_length=256
                    )
                    analyse_sound_data.analyse_audio()

                # delete file
                if delete_data:
                    print(f'Deleting segment file {segment_path}...')
                    os.remove(segment_path)

            except Exception as e:
                print('  Error when creating segment: ' + str(e))
        print('Done')
