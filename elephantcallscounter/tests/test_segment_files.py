import os

from elephantcallscounter.adapters.azure_interface import AzureInterface
from elephantcallscounter.services.data_processing_service import create_file_segments
from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths


class TestFileSegments:
    def test_create_file_segments(self):
        """ This tests the create_file_segments method.

        :raises AssertionError:
        :return void:
        """
        file_path = join_paths(
            [get_project_root(), 'tests/test_fixtures/test_training_set.txt']
        )
        azure_interface = AzureInterface('elephant-sound-data')
        azure_interface.download_from_azure(
            'TestSet/nn01d/nn01d_20180127_000000.wav',
            join_paths(
                [get_project_root(), 'data/segments/TrainingSet/nn01d/nn01d_20180127_000000.wav']
            )
        )
        azure_interface.download_from_azure(
            'TrainingSet/nn01b/nn01b_20180220_000000.wav',
            join_paths(
                [get_project_root(), 'data/segments/TrainingSet/nn01b/nn01b_20180220_000000.wav']
            )
        )
        assert create_file_segments(
            file_path
        )
        assert len(os.listdir(
            join_paths([get_project_root(), 'data/segments/CroppedTrainingSet/nn01d'])
        )) == 3
        assert len(os.listdir(
            join_paths([get_project_root(), 'data/segments/CroppedTrainingSet/nn01b'])
        )) == 4
