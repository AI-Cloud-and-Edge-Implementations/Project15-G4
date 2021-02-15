import os
import pandas as pd
from pydub import AudioSegment
from elephantcallscounter.data_processing.audio_processing import AudioProcessing


class FileSegmenter:
    def __init__(self):
        pass

    @staticmethod
    def crop_all_files(list_of_files):
        for start_time, end_time, file, cropped_file in list_of_files:
            AudioProcessing.crop_file(
                start_time,
                end_time,
                file_name=file,
                destination_file=cropped_file
            )

    @staticmethod
    def segment_files():
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
            print(f'Processing {filename}...')

            file = AudioSegment.from_wav('data/raw/' + filename)

            print(f'Processing file data/raw/{filename}...')

            # get the relevant segments from the metadata
            metadata_segments = metadata[metadata['filename'] == filename]

            for index, metadata_segment in metadata_segments.iterrows():
                try:
                    selection = metadata_segment["Selection"]
                    print(f' Generating segment {selection}...')

                    start = (metadata_segment['File Offset (s)'] * 1000) - slack_time  # ms
                    duration = (metadata_segment['duration'] * 1000) + (slack_time * 2)  # ms
                    end = start + duration

                    segment = file[start:end]

                    marginal = str(metadata_segment['marginals']).strip()
                    segment_path = f'data/segments/{train_or_test}/{filename}_segment_{selection}_{marginal}.wav'
                    segment.export(segment_path, format='wav')
                    print(f' Found segment of {segment.duration_seconds} seconds, exported to {segment_path}.')
                except Exception as e:
                    print('  Error when creating segment: ' + str(e))

            print('Done')
