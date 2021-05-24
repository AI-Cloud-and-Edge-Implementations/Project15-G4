import asyncio
import logging
import multiprocessing
import requests
import time

from elephantcallscounter.adapters.shared.audio_events_queue import AudioEventsQueue
from elephantcallscounter.iot.send_data_to_cloud import write_to_hub
from elephantcallscounter.iot.read_data_from_cloud import ReadDataFromCloud
from elephantcallscounter.utils.concurrency import run_in_parallel
from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths
from elephantcallscounter.utils.file_utils import get_files_in_dir

logger = logging.getLogger(__name__)


def send_to_iot(source_dir, flag, container_name, dest_folder):
    path = join_paths([get_project_root(), source_dir])
    spectrogram_list = get_files_in_dir(path)
    counter = {"count": 0}
    # Add a delay to let the receiver catch up.
    time.sleep(10)
    asyncio.run(
        write_to_hub(
            path,
            spectrogram_list,
            counter,
            limit=len(spectrogram_list),
            container_name=container_name,
            dest_folder=dest_folder,
        )
    )
    logger.info("finished sending data!!!")
    flag["finished"] = True


def receive_from_iot(queue_name, flag, dest_folder):
    audio_events_queue = AudioEventsQueue(queue_name)
    read_data_from_cloud = ReadDataFromCloud(
        audio_events_queue=audio_events_queue, flag=flag, dest_folder=dest_folder
    )
    read_data_from_cloud.consume_events()


def device_simulator(source_dir, container_name, queue_name, dest_folder):
    manager = multiprocessing.Manager()
    flag = manager.dict({"finished": False})
    run_in_parallel(
        lambda: send_to_iot(source_dir, flag, container_name, dest_folder),
        lambda: receive_from_iot(queue_name, flag, dest_folder),
    )
    logger.info("Finished receiving about to run inference")
    try:
        requests.get(
            "http://0.0.0.0:5000/blob_events/run_pipeline/",
            params={"queue_name": queue_name, "container_name": container_name},
        )
        logger.info("Running inference")
    except requests.exceptions.ConnectionError:
        logger.info("Error in connecting to blob events endpoint.")
