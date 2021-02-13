import os
import pandas as pd
from pydub import AudioSegment

from elephantcallscounter.data_processing.audio_processing import AudioProcessing
from elephantcallscounter.utils.data_structures import RangeSet


class SegmentFiles:
    def __init__(self, file_range=30):
        self.file_range = file_range

    @staticmethod
    def crop_all_files(list_of_files):
        """ Generate file crops based on input files.

        :param list_of_files:
        :return:
        """

        for start_time, end_time, file, cropped_file in list_of_files:
            AudioProcessing.crop_file(
                start_time,
                end_time,
                file_name = file,
                destination_file = cropped_file
            )

    @staticmethod
    def generate_file_name(actual_file, start_time, end_time, extension):
        return actual_file + '_' + str(start_time) + "_" + str(end_time) + '_cropped.' + extension

    @staticmethod
    def split_metadata_into_groups(metadata):
        file_groups = metadata.groupby('filename')
        file_dfs = [file_groups.get_group(x) for x in file_groups.groups]

        return file_dfs

    def ready_file_segments(
            self,
            metadata_filepath = 'data/metadata/nn_ele_hb_00-24hr_TrainingSet_v2.txt'
    ):
        """ This method readies the file segments for further processing.

        :param metadata_filepath:
        :return:
        """
        # read metadata
        metadata = pd.read_csv(metadata_filepath, sep='\t', header=0)
        print(f'Using metadata file {metadata_filepath}')

        files_to_crop = []

        metadata['file_start_times'] = metadata['File Offset (s)'] - self.file_range
        metadata['file_end_times'] = metadata['File Offset (s)'] + self.file_range
        file_dfs = self.split_metadata_into_groups(metadata)
        for file_metadata in file_dfs:
            start_end_times = RangeSet()
            for index, row in file_metadata.iterrows():
                file_name = row['filename']
                actual_file, extension = file_name.split(".")
                start_time = row['file_start_times']
                end_time = row['file_end_times']
                if start_end_times.data_in_range(time_range = (start_time, end_time)):
                    start_end_times.insert_data((start_time, end_time))
                    cropped_file_name = self.generate_file_name(
                        actual_file, start_time, end_time, extension
                    )
                    files_to_crop.append((start_time, end_time, file_name, cropped_file_name))

        return files_to_crop

    def segment_files(self, az_container):
        container_name = 'elephant-sound-data'

        blob_container_client = az_container.connect_to_container()

        # read metadata
        metadata_filepath = 'data/metadata/nn_ele_hb_00-24hr_TrainingSet_v2.txt'
        metadata = pd.read_csv(metadata_filepath, sep='\t', header=None)
        print(f'Using metadata file {metadata_filepath}')

        # process raw files
        for blob in blob_container_client.list_blobs():
            filename = blob.name
            print(f'Processing {filename}...')

            blob_client = blob_container_client.get_blob_client(blob=filename)

            # download file
            download_path = 'data/' + filename
            with open(download_path, 'wb') as download_file:
                dir = download_path.split('/')[-1]
                if (not os.path.exists(dir)):
                    print(f' Creating directory {dir}...')
                    os.mkdir(dir)

                print(f' Downloading {download_path}...')
                download_file.write(blob_client.download_blob().readall())

            file = AudioSegment.from_wav(download_path)

            print(f'Processing blob {x}...')

            # get the relevant segments from the metadata
            metadata_segments = metadata[metadata['filename'] == filename]

            for index, metadata_segment in metadata_segments.iterrows():
                try:
                    selection = metadata_segment["Selection"].lstrip()
                    print(f' Generating segment {selection}...')

                    start = metadata_segment['File Offset (s)']  # ms
                    duration = metadata_segment['duration'] * 1000  # ms
                    end = start + duration

                    segment = file[start:end]

                    marginal = str(metadata_segment['marginals']).strip()
                    segment_path = f'segments/{filename}_segment_{selection}_{marginal}.wav'
                    segment.export(segment_path, format='wav')
                    print(f' Found segment of {segment.duration_seconds} seconds, exported to {segment_path}.')
                except Exception as e:
                    print('  Error when creating segment: ' + str(e))

            # remove local file
            os.remove(download_path)

            print('Done')
