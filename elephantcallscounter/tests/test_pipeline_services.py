from elephantcallscounter.services.pipeline_services import pipeline_run

from elephantcallscounter.utils.file_utils import get_files_in_dir
from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths


class TestPipelineServices:
    def test_run_pipeline(self):
        for file in get_files_in_dir('tests/test_fixtures/'):
            assert pipeline_run(
                join_paths([get_project_root(), 'tests/test_fixtures/', file]),
                'data/demo/test_spec_image_labels.csv'
            ) == 1
