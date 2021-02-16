import pandas as pd
import os


class MetadataProcessing:
    def __init__(self, metadata_filepath):
        self.metadata_filepath = metadata_filepath

    def load_metadata(self):
        """ Calculate start and end file timestamps.

        :return void :
        """
        # read metadata
        metadata = pd.read_csv(self.metadata_filepath, sep='\t', header=0)
        print(f'Using metadata file {self.metadata_filepath}')
        return metadata

