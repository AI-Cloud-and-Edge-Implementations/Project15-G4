import asyncio

from elephantcallscounter.adapters.shared.audio_events_queue import AudioEventsQueue
from elephantcallscounter.iot.send_data_to_cloud import write_to_hub
from elephantcallscounter.iot.read_data_from_cloud import ReadDataFromCloud
from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths
from elephantcallscounter.utils.file_utils import get_files_in_dir


def send_to_iot(source_dir = "data/spectrogram_bb/1/"):
    path = join_paths([get_project_root(), source_dir])
    spectrogram_list = get_files_in_dir(path)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(write_to_hub(path, spectrogram_list))


def receive_from_iot(container_name, queue_name, dest_folder):
    audio_events_queue = AudioEventsQueue(queue_name)
    read_data_from_cloud = ReadDataFromCloud(
        container_name = container_name,
        audio_events_queue = audio_events_queue,
        dest_folder = dest_folder
    )
    read_data_from_cloud.consume_events()
