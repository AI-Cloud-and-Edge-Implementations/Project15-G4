import csv
import os


from elephantcallscounter.utils.path_utils import get_project_root, join_paths


def write_to_csv(data, file_name):
    """ Function to write data to csv file.
    :param list data:
    :param string file_name:
    :return void:
    """
    with open(file_name, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter = ',')
        for line in data:
            writer.writerow(line)


def write_to_bin_file(data, file_name):
    """ Function to write data to binary file.

    :param data:
    :param file_name:
    :return:
    """
    with open(file_name, 'wb') as bin_file:
        bin_file.write(data)


def get_files_in_dir(path):
    return os.listdir(join_paths([get_project_root(), path]))


def delete_images(directories, file_name):
    for directory in directories:
        os.remove(join_paths([get_project_root(), directory, file_name]))
