from flask import Blueprint
from flask import request
from elephantcallscounter.adapters.shared.audio_events_queue import AudioEventsQueue
from elephantcallscounter.adapters.azure_interface import AzureInterface
from elephantcallscounter.services.pipeline_services import pipeline_run

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
    messages = [message for message in messages]
    for message in messages:
        file_path = message['content'].split('/')[-1]
        azure_interface.download_from_azure(
            message['content'],
            dest_file = file_path
        )
        print('about to run pipeline on {}!'.format(file_path))
        pipeline_run(file_path, 'data/labels/spec_images_labels.csv')
