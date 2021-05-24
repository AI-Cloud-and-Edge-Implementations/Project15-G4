from elephantcallscounter.data_processing.metadata_processing import \
    MetadataProcessing
from elephantcallscounter.data_processing.segment_files import SegmentFiles


def create_file_segments(file_name):
    metadata = MetadataProcessing(metadata_filepath=file_name)
    segment_files = SegmentFiles(False)
    segment_files.process_segments(
        segment_files.ready_file_segments(metadata.load_metadata())
    )
