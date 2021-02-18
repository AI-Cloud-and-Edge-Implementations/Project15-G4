from pathlib import Path


def get_project_root():
    """ Function to return the roo location of the project.
    :return string:
    """
    return Path(__file__).parent.parent


def split_file_path(strng, sep, pos):
    """ This method splits the path on seperator at the respective position.

    :param strng:
    :param sep:
    :param pos:
    :return strng:
    """
    strng = strng.split(sep)
    return sep.join(strng[:pos]), sep.join(strng[pos:])

