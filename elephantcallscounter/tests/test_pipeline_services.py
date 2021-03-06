from elephantcallscounter.services.pipeline_services import pipeline_run


class TestPipelineServices:
    def test_run_pipeline(self):
        assert pipeline_run(
            'tests/test_fixtures/nn01a_20180126_000000_48835100.0_48895100.0_cropped.wav',
            'data/demo/test_spec_image_labels.csv'
        ) == 1

