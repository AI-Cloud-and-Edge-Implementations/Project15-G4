from pathlib import Path


def get_project_root():
    """ Function to return the roo location of the project.
    :return string:
    """
    return Path(__file__).parent.parent
