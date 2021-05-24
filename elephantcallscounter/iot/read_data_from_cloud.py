import ast
import asyncio
import logging

from azure.eventhub.aio import EventHubConsumerClient

from elephantcallscounter.config import env
from elephantcallscounter.utils.path_utils import join_paths

logger = logging.getLogger(__name__)


class ReadDataFromCloud:
    def __init__(self, audio_events_queue, flag, dest_folder):
        """Read data from iot hub and send to queue.

        :param elephantcallscounter.adapters.shared.AudioEventsQueue:
        :param dict flag:
        :param string dest_folder:
        """
        self.audio_events_queue = audio_events_queue
        self.url_location = "http://0.0.0.0:5000/blob_events/run_pipeline/"
        self.flag = flag
        self.dest_folder = dest_folder

    async def on_event_batch(self, partition_context, events):
        for event in events:
            logger.info("Got new event to process!")
            event_data = ast.literal_eval(event.body_as_str())
            logger.info("Received file name in queue: %s", event_data["filename"])
            self.audio_events_queue.insert_message_queue(
                join_paths([self.dest_folder, event_data["filename"]])
            )

        if self.flag["finished"]:
            import sys

            sys.exit(0)

        await partition_context.update_checkpoint()

    async def on_error(self, partition_context, error):
        if partition_context:
            logger.info(
                "An exception: {} occurred during receiving from Partition: {}.".format(
                    partition_context.partition_id, error
                )
            )
        else:
            logger.info(
                "An exception: {} occurred during the load balance process.".format(
                    error
                )
            )

    def consume_events(self):
        loop = asyncio.get_event_loop()
        client = EventHubConsumerClient.from_connection_string(
            conn_str=env.EVENTHUB_CONN_STRING, consumer_group="$default"
        )
        try:
            loop.run_until_complete(
                client.receive_batch(
                    on_event_batch=self.on_event_batch, on_error=self.on_error
                )
            )
        except KeyboardInterrupt:
            logger.info("Receiving has stopped.")
        finally:
            logger.info("Receiving has finished.")
            loop.run_until_complete(client.close())
            loop.stop()
