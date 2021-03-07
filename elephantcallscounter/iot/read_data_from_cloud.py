import asyncio
import ast
from azure.eventhub.aio import EventHubConsumerClient
import logging
import requests

from elephantcallscounter.adapters.azure_interface import AzureInterface
from elephantcallscounter.config import env
from elephantcallscounter.utils.file_utils import write_to_bin_file
from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths

logger = logging.getLogger(__name__)


class ReadDataFromCloud:
    def __init__(self, container_name, audio_events_queue, dest_folder, flag):
        """ Read data from iot hub and send to queue.

        :param string container_name:
        :param elephantcallscounter.adapters.shared.AudioEventsQueue:
        :param string  dest_folder:
        """
        self.audio_events_queue = audio_events_queue
        self.container_name = container_name
        self.dest_folder = dest_folder
        self.url_location = 'http://0.0.0.0:5000/blob_events/run_pipeline/'
        self.flag = flag

    async def on_event_batch(self, partition_context, events):
        for event in events:
            logger.info("Got new event to process!")
            event_data = ast.literal_eval(event.body_as_str())
            logger.info("Received file name in queue: %s", event_data['filename'])
            file_path = join_paths(
                [
                    get_project_root(),
                    'data/imported_data/' + event_data['filename']
                ]
            )
            write_to_bin_file(
                bytes(event_data['filecontent'], 'utf-8'),
                file_path
            )
            self.audio_events_queue.insert_message_queue(
                join_paths([self.dest_folder, event_data['filename']])
            )
            azure_interface = AzureInterface(self.container_name)
            azure_interface.send_to_azure(
                file_path, self.dest_folder, event_data['filename']
            )

        if self.flag['finished']:
            import sys
            sys.exit(0)

        await partition_context.update_checkpoint()

    async def on_error(self, partition_context, error):
        if partition_context:
            logger.info("An exception: {} occurred during receiving from Partition: {}.".format(
                partition_context.partition_id,
                error
            ))
        else:
            logger.info("An exception: {} occurred during the load balance process.".format(error))

    def consume_events(self):
        loop = asyncio.get_event_loop()
        client = EventHubConsumerClient.from_connection_string(
            conn_str = env.EVENTHUB_CONN_STRING,
            consumer_group = "$default"
        )
        try:
            loop.run_until_complete(
                client.receive_batch(on_event_batch = self.on_event_batch, on_error = self.on_error)
            )
        except KeyboardInterrupt:
            logger.info("Receiving has stopped.")
        finally:
            logger.info('Receiving has finished.')
            loop.run_until_complete(client.close())
            loop.stop()
