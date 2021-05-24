import functools
import os
from pathlib import Path


def get_project_root():
    """Function to return the roo location of the project.
    :return string:
    """
    return Path(__file__).parent.parent


def split_file_path(strng, sep, pos):
    """This method splits the path on seperator at the respective position.

    :param strng:
    :param sep:
    :param pos:
    :return strng:
    """
    strng = strng.split(sep)
    return sep.join(strng[:pos]), sep.join(strng[pos:])


def join_paths(paths):
    return functools.reduce(os.path.join, paths)


def create_necessary_directories(save_loc):
    """This method creates the necessary directory structure.

    :return void:
    """
    Path(save_loc).mkdir(parents=True, exist_ok=True)


class FilePaths:
    def __init__(self, folder_path, file_name):
        self.folder_path = folder_path
        self.file_name = file_name

    def path(self):
        return self.folder_path + "/" + self.file_name

    def __hash__(self):
        return hash(self.path())
