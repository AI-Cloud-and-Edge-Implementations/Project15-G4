from collections import defaultdict
from researchanddevelopment.config import env
import logging
import pandas as pd
import subprocess
import os


class FilePaths:
    def __init__(self, folder_path, file_name):
        self.folder_path = folder_path
        self.file_name = file_name

    def path(self):
        return self.folder_path + "/" + self.file_name

    def __hash__(self):
        return hash(self.path())


class AzureDataImporter:
    def __init__(self, source_directory):
        self._logger = logging.getLogger('az-copy-data-from-s3')
        logging.basicConfig(level=logging.INFO)
        self._sas_key = env.STORAGE_SAS_KEY
        self._source_directory = source_directory

    def az_copy_data_from_s3(self, source_file_path, destination_file_path):
        """ This method handles the copying of data between two urls paths.

        :param source_file_path:
        :param destination_file_path:
        :return None:
        """
        self._logger.info("Sending file from {} to {}".format(
            source_file_path, destination_file_path
        ))
        amazon_path = "https://s3.us-west-2.amazonaws.com/congo8khz-pnnn/recordings/wav/{}".format(
            source_file_path
        )
        azure_path = "https://project15.blob.core.windows.net/elephant-sound-data/{}/{}".format(
            destination_file_path,
            self._sas_key
        )
        command_to_run = ['azcopy', 'cp', amazon_path, azure_path, '--recursive']
        self._logger.info('We ran this command: {0}'.format(' '.join(command_to_run)))
        subprocess.run(command_to_run)
        self._logger.info("Completed Copying File: {}".format(source_file_path))

    def process_files(self):
        """ Process the files from the source directory.

        :return void:
        """
        file_data_pairs = []
        processed_file_map = defaultdict(list)
        for input_file in os.listdir(self._source_directory):
            file_data_pairs.append(
                (
                    os.path.splitext(input_file)[0],
                    self.get_unique_file_names(
                        self.read_file(os.path.join(self._source_directory, input_file))
                    )
                )
            )

        for file_pairs in file_data_pairs:
            for file_path in file_pairs[1]:
                folder_path, _ = self.separate_folder_file_path(file_path)
                dest_path = FilePaths(file_pairs[0], folder_path)
                processed_file_map[dest_path].append(FilePaths(folder_path, file_path))

        return processed_file_map

    @staticmethod
    def read_file(file_name):
        """ Read the tab delimited csv file and return a pandas dataframe.

        :param string file_name:
        :return pandas.dataframe:
        """
        file_data = pd.read_csv(file_name, delimiter="\t")
        return file_data

    @staticmethod
    def get_unique_file_names(elephant_table):
        """ Get the unique file names from the series of file names in the data.

        :param pandas.dataframe elephant_table:
        :return list:
        """
        seen = {}
        return [
            seen.setdefault(file, file) for file in elephant_table['filename'].tolist() if file not in seen
        ]

    @staticmethod
    def separate_folder_file_path(file_path):
        """ Seperate the file path into two.

        :param string file_path:
        :return tuple:
        """
        return file_path.split("_", 1)

    def send_to_copy_handler(self):
        processed_file_map = self.process_files()
        for dest_path, source_paths in processed_file_map.items():
            self._logger.info("Total Number of files for {}".format(dest_path.folder_path, len(source_paths)))
            for source_path in source_paths:
                self.az_copy_data_from_s3(source_path.path(), dest_path.path())


def main():
    az_data_importer = AzureDataImporter(source_directory='rumble_landscape_general')
    az_data_importer.send_to_copy_handler()


if __name__ == '__main__':
    main()
