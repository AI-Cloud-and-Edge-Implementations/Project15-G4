import asyncio

from elephantcallscounter.iot.send_data_to_cloud import write_to_hub
from elephantcallscounter.iot.read_data_from_cloud import consume_events
from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths
from elephantcallscounter.utils.file_utils import get_files_in_dir


def send_to_iot(source_dir = "data/spectrogram_bb/test/1/"):
    path = join_paths([get_project_root(), source_dir])
    spectrogram_list = get_files_in_dir(path)
    asyncio.run(write_to_hub(path, spectrogram_list))


def receive_from_iot():
    consume_events()
