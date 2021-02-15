import csv


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
