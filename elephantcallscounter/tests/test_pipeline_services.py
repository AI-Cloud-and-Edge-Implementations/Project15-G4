from elephantcallscounter.services.pipeline_services import pipeline_run

from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths


class TestPipelineServices:
    def test_run_pipeline(self):
        value = pipeline_run(
            join_paths([get_project_root(), "tests/test_fixtures/"]),
            "data/demo/test_spec_image_labels.csv",
        )
        assert value[0] == 1
        assert value[1] == 1
        assert value[2] == 1
