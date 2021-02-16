import os

from elephantcallscounter.data_import.az_copy import AzureDataImporter
from elephantcallscounter.data_processing.segment_files import SegmentFiles
from elephantcallscounter.data_processing.segment_files import FileSegmenter
from elephantcallscounter.utils.path_utils import get_project_root


def create_file_segments(delete_data: bool = False):
    FileSegmenter.segment_files(delete_data)


def create_file_segments_az_data_importer():
    segment_files = SegmentFiles(az_data_importer, False)
    segment_files.process_segments(segment_files.ready_file_segments())
