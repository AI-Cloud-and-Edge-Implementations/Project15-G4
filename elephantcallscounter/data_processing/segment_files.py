from collections import defaultdict
import os
import pandas as pd

from elephantcallscounter.data_processing.audio_processing import AudioProcessing
from elephantcallscounter.utils.data_structures import RangeSet
from elephantcallscounter.utils.path_utils import get_project_root


class SegmentFiles:
    def __init__(self, az_importer, file_range=30):
        """ This class handles the segmentation of files after reading from azure.

        :param elephantcallscounter.data_import.az_copy.AzureDataImporter az_importer:
        :param int file_range:
        """
        self.file_range = file_range
        self.az_importer = az_importer

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
            metadata_filepath = os.path.join(
                get_project_root(), 'data/metadata/nn_ele_hb_00-24hr_TrainingSet_v2.txt'
            )
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
                    folder_path = file_name.split("_")[0]
                    file_name = os.path.join(folder_path, file_name)
                    cropped_file_name = os.path.join(folder_path, cropped_file_name)
                    files_to_crop.append((start_time, end_time, file_name, cropped_file_name))

        return files_to_crop

    def process_segments(self, files_to_crop):
        folder_based_grouping = defaultdict(list)
        for file_data in files_to_crop:
            folder_based_grouping[file_data[2]].append(file_data)

        for filename, folder_files in folder_based_grouping.items():
            folder_name = filename.split('/')[0]
            source_folder = os.path.join('TrainingSet', folder_name)
            dest_folder = os.path.join(
                get_project_root(), 'data', 'segments', 'TrainingSet', folder_name
            )
            print(f'Processing {source_folder}...')
            """
            p1 = self.az_importer.az_download_data_from_blob(
                source_path = source_folder,
                destination_path = dest_folder
            )
            """
            print(f'Processing {source_folder} finished!')
            os.makedirs(
                os.path.join(
                    get_project_root(), 'data', 'segments', 'CroppedTrainingSet',
                    folder_name
                ), exist_ok = True,
            )
            original_file = os.path.join(
                get_project_root(), 'data', 'segments', 'TrainingSet', filename
            )
            for file_data in folder_files:
                cropped_file = os.path.join(
                    get_project_root(), 'data', 'segments', 'CroppedTrainingSet', file_data[3]
                )
                AudioProcessing.crop_file(
                    file_data[0],
                    file_data[1],
                    file_name = original_file,
                    destination_file = cropped_file
                )

                print('Done')

            # remove local file
            os.remove(original_file)

