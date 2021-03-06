from elephantcallscounter.services.events_services import device_simulator
from elephantcallscounter.services.pipeline_services import pipeline_run

from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths


class TestPipelineServices:
    def test_run_pipeline(self):
        device_simulator(
            source_dir = 'tests/test_fixtures/',
            container_name = 'elephant-sound-data',
            queue_name = 'realtimequeue',
            dest_folder = 'realtimeblobs'
        )
        assert pipeline_run(
            'tests/test_fixtures/nn01a_20180126_000000_48835100.0_48895100.0_cropped.wav',
            'data/demo/test_spec_image_labels.csv'
        ) == 1
