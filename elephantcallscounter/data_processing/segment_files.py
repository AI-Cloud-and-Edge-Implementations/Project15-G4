import os
import pandas as pd
from pydub import AudioSegment

from elephantcallscounter.data_processing.audio_processing import AudioProcessing


class SegmentFiles:
    def crop_all_files(self, list_of_files):
        for start_time, end_time, file, cropped_file in list_of_files:
            AudioProcessing.crop_file(
                start_time,
                end_time,
                file_name = file,
                destination_file = cropped_file
            )

    def ready_file_segments(self, metadata_filepath = 'data/metadata/nn_ele_hb_00-24hr_TrainingSet_v2.txt'):
        # read metadata
        metadata = pd.read_csv(metadata_filepath, sep='\t', header=0)
        print(f'Using metadata file {metadata_filepath}')

        files = []

        file_names = set()

        file_min_start_times = metadata.groupby('filename')['File Offset (s)'].min()
        file_min_end_times = metadata.groupby('filename')['File Offset (s)'].max()
        for index, row in metadata.iterrows():
            if row['filename'] not in file_names:
                file_name = row['filename']
                actual_file, extension = file_name.split(".")
                cropped_file_name = actual_file + '_cropped.' + extension
                start_time = file_min_start_times[file_name]
                end_time = file_min_end_times[file_name]
                files.append((start_time, end_time, file_name, cropped_file_name))
                file_names.add(file_name)

        print(files)

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
