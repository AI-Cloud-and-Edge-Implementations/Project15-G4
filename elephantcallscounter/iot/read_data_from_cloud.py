import asyncio
import ast
from azure.eventhub.aio import EventHubConsumerClient

from elephantcallscounter.config import env
from elephantcallscounter.services.data_import_service import copy_file_to_azure_fast
from elephantcallscounter.utils.file_utils import write_to_bin_file
from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths


class ReadDataFromCloud:
    def __init__(self, container_name, audio_events_queue, dest_folder):
        """ Read data from iot hub and send to queue.

        :param string container_name:
        :param elephantcallscounter.adapters.shared.AudioEventsQueue:
        :param string  dest_folder:
        """
        self.audio_events_queue = audio_events_queue
        self.container_name = container_name
        self.dest_folder = dest_folder

    async def on_event_batch(self, partition_context, events):
        for event in events:
            event_data = ast.literal_eval(event.body_as_str())
            print("Received event from partition: {}.".format(partition_context.partition_id))
            print("Telemetry received: ", event.body_as_str())
            print("Properties (set by device): ", event.properties)
            print("System properties (set by IoT Hub): ", event.system_properties)
            print("File name in queue: ", event_data['filename'])
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
            copy_file_to_azure_fast(self.container_name, file_path, self.dest_folder)

        await partition_context.update_checkpoint()

    async def on_error(self, partition_context, error):
        # Put your code here. partition_context can be None in the on_error callback.
        if partition_context:
            print("An exception: {} occurred during receiving from Partition: {}.".format(
                partition_context.partition_id,
                error
            ))
        else:
            print("An exception: {} occurred during the load balance process.".format(error))

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
            print("Receiving has stopped.")
        finally:
            loop.run_until_complete(client.close())
            loop.stop()
