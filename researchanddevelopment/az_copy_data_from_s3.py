from collections import defaultdict
import logging
import pandas as pd
import subprocess
import os

SAS_KEY = "?sv=2019-12-12&ss=bfqt&srt=sco&sp=rwdlacupx&se=2021-01-16T08:16:45Z&st=2021-01-16T00:16:45Z&spr=https&sig=R3uZmb%2BA1BK%2FwGzwOtSPU4CaLVklOkExKCmKAMrAWQs%3D"
logger = logging.getLogger('az-copy-data-from-s3')
logging.basicConfig(level=logging.INFO)


class FilePaths:
    def __init__(self, folder_path, file_name):
        self.folder_path = folder_path
        self.file_name = file_name

    def path(self):
        return self.folder_path + "/" + self.file_name

    def __hash__(self):
        return hash(self.path())


def az_copy_data_from_s3(source_file_path, destination_file_path):
    logger.info("Sending file from {} to {}".format(source_file_path, destination_file_path))
    amazon_path = "https://s3.us-west-2.amazonaws.com/congo8khz-pnnn/recordings/wav/{}".format(source_file_path)
    azure_path = "https://project15storage.blob.core.windows.net/elephant-sound-accurate/{}/{}".format(
        destination_file_path,
        SAS_KEY
    )
    command_to_run = ['azcopy', 'cp', amazon_path, azure_path, '--recursive']
    logger.info('We ran this command: {0}'.format(' '.join(command_to_run)))
    subprocess.run(command_to_run)
    logger.error("Completed Copying File: {}".format(source_file_path))


def read_file(file_name):
    file_data = pd.read_csv(file_name, delimiter="\t")
    return file_data


def get_unique_file_names(elephant_table):
    seen = {}
    return [seen.setdefault(file, file) for file in elephant_table['filename'].tolist() if file not in seen]


def seperate_folder_file_path(file_path):
    return file_path.split("_", 1)


def process_files():
    file_data_pairs = []
    processed_file_map = defaultdict(list)
    for input_file in os.listdir('rumble_landscape_general'):
        file_data_pairs.append(
            (
                os.path.splitext(input_file)[0],
                get_unique_file_names(
                    read_file(os.path.join('rumble_landscape_general', input_file))
                )
            )
        )

    for file_pairs in file_data_pairs:
        for file_path in file_pairs[1]:
            folder_path, _ = seperate_folder_file_path(file_path)
            dest_path = FilePaths(file_pairs[0], folder_path)
            processed_file_map[dest_path].append(FilePaths(folder_path, file_path))

    return processed_file_map


def send_to_copy_handler(processed_file_map):
    for dest_path, source_paths in processed_file_map.items():
        logger.info("Total Number of files for {}".format(dest_path.folder_path, len(source_paths)))
        for source_path in source_paths:
            az_copy_data_from_s3(source_path.path(), dest_path.path())


def main():
    send_to_copy_handler(process_files())


if __name__ == '__main__':
    main()
