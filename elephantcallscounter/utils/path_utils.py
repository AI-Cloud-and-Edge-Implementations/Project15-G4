import csv
from pathlib import Path


def get_project_root():
    """ Function to return the roo location of the project.
    :return string:
    """
    return Path(__file__).parent.parent


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
