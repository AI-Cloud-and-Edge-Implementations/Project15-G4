from collections import defaultdict
import os

from elephantcallscounter.data_processing.audio_processing import AudioProcessing
from elephantcallscounter.utils.data_structures import RangeSet
from elephantcallscounter.utils.path_utils import get_project_root


class SegmentFiles:
    def __init__(self, start_fresh, file_range=30):
        """ This class handles the segmentation of files after reading from azure.

        :param elephantcallscounter.data_import.az_copy.AzureDataImporter az_importer:
        :param bool start_fresh:
        :param int file_range:
        """
        self.file_range = file_range
        self.start_fresh = start_fresh
        self.training_set = os.path.join(get_project_root(), 'data', 'segments', 'TrainingSet')
        self.crop_set = os.path.join(get_project_root(), 'data', 'segments', 'CroppedTrainingSet')

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
            metadata
    ):
        """ This method readies the file segments for further processing.

        :param pandas.DataFrame metadata:
        :return:
        """
        files_to_crop = []
        # Removing outliers
        metadata.drop(metadata[metadata.duration > 1000].index, inplace = True)
        metadata['file_start_times'] = metadata['File Offset (s)']*1000 - self.file_range*1000
        metadata['file_end_times'] = metadata['File Offset (s)']*1000 + self.file_range*1000

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

    def crop_files(self, folder_files):
        for file_data in folder_files:
            original_file = os.path.join(
                self.training_set, file_data[2]
            )
            cropped_file = os.path.join(
                self.crop_set, file_data[3]
            )
            is_cropped = AudioProcessing.crop_file(
                file_data[0],
                file_data[1],
                file_name = original_file,
                destination_file = cropped_file
            )
            if is_cropped:
                print('Cropped File: ', cropped_file)

    def clear_segments(self):
        for folder in os.listdir(self.training_set):
            for file in os.listdir(os.path.join(self.training_set, folder)):
                os.remove(file)
        for folder in os.listdir(self.crop_set):
            for file in os.listdir(os.path.join(self.crop_set, folder)):
                os.remove(file)

    def process_segments(self, files_to_crop):
        folder_based_grouping = defaultdict(list)
        for file_data in files_to_crop:
            folder_name = file_data[2].split('/')[0]
            folder_based_grouping[folder_name].append(file_data)

        if self.start_fresh:
            self.clear_segments()

        for folder_name, folder_files in folder_based_grouping.items():
            os.makedirs(os.path.join(self.crop_set, folder_name), exist_ok = True)
            files_to_delete = os.path.join(self.training_set, folder_name)
            self.crop_files(folder_files)

            # remove local file
            for file_to_remove in os.listdir(files_to_delete):
                os.remove(os.path.join(files_to_delete, file_to_remove))
                print("File removed: ", file_to_remove)
