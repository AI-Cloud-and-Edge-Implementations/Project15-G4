import pandas as pd
import logging


logger = logging.getLogger(__name__)


class MetadataProcessing:
    def __init__(self, metadata_filepath):
        self.metadata_filepath = metadata_filepath

    def load_metadata(self):
        """ Calculate start and end file timestamps.

        :return void :
        """
        # read metadata
        metadata = pd.read_csv(self.metadata_filepath, sep='\t', header=0)
        # Removing outliers
        metadata.drop(metadata[metadata.duration > 1000].index, inplace = True)
        logger.info(f'Using metadata file {self.metadata_filepath}')
        return metadata

    @classmethod
    def split_metadata_into_groups(cls, metadata):
        file_groups = metadata.groupby('filename')
        file_dfs = [file_groups.get_group(x) for x in file_groups.groups]

        return file_dfs

