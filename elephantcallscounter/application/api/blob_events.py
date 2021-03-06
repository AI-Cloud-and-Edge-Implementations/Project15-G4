from flask import Blueprint
from flask import request
from elephantcallscounter.adapters.shared.audio_events_queue import AudioEventsQueue
from elephantcallscounter.adapters.azure_interface import AzureInterface
from elephantcallscounter.management.commands.pipeline_commands import run_demo
from elephantcallscounter.utils.path_utils import join_paths
from elephantcallscounter.utils.path_utils import get_project_root

blob_blueprint = Blueprint(
    'blob_events',
    __name__,
    url_prefix = '/blob_events'
)


@blob_blueprint.route('/run_pipeline/', methods = ['GET'])
def run_processing():
    queue_name = request.args.get('queue_name')
    container_name = request.args.get('container_name')
    audio_events_queue = AudioEventsQueue(queue_name)
    messages = audio_events_queue.dequeue_message_queue()
    azure_interface = AzureInterface(container_name = container_name)
    for message in messages:
        file_path = message['Message Text']
        azure_interface.download_from_azure(
            file_path,
            dest_file = join_paths([get_project_root(), file_path.split('/')[-1]])
        )
        run_demo(file_path)

    return
