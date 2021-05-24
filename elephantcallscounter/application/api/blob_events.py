import logging

from flask import Blueprint, request

from elephantcallscounter.adapters.azure_interface import AzureInterface
from elephantcallscounter.adapters.shared.audio_events_queue import \
    AudioEventsQueue
from elephantcallscounter.services.pipeline_services import pipeline_run
from elephantcallscounter.utils.path_utils import get_project_root, join_paths

blob_blueprint = Blueprint("blob_events", __name__, url_prefix="/blob_events")

logger = logging.getLogger(__name__)


@blob_blueprint.route("/run_pipeline/", methods=["GET"])
def run_processing():
    queue_name = request.args.get("queue_name")
    container_name = request.args.get("container_name")
    audio_events_queue = AudioEventsQueue(queue_name)
    messages = audio_events_queue.dequeue_message_queue()
    azure_interface = AzureInterface(container_name=container_name)
    messages = [message for message in messages]
    for message in messages:
        file_path = message["content"].split("/")[-1]
        file_path = join_paths([get_project_root(), "data/imported_data", file_path])
        azure_interface.download_from_azure(message["content"], dest_file=file_path)
    logger.info("about to run pipeline on {}!".format("data/imported_data"))
    pipeline_run("data/imported_data", "data/labels/spec_images_labels.csv")
    audio_events_queue.delete_processed_messages(messages)
    logger.info("Deleted processed messages")
    return {}
