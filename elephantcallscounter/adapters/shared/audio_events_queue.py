import logging

from azure.core.exceptions import HttpResponseError, ResourceExistsError
from azure.storage.queue import QueueClient, BinaryBase64EncodePolicy, BinaryBase64DecodePolicy

from elephantcallscounter.config import env

logger = logging.getLogger(__name__)


class AudioEventsQueue:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.queue_client = QueueClient.from_connection_string(
            env.CONNECTION_STRING, self.queue_name
        )
        self.create_queue()

    def create_queue(self):
        # Instantiate a QueueClient object which will
        # be used to create and manipulate the queue
        logger.info("Creating queue: " + self.queue_name)
        # Create the queue
        try:
            self.queue_client.create_queue()
        except ResourceExistsError:
            logger.info('Queue {} already exists!'.format(self.queue_name))
        except HttpResponseError:
            logger.info('Invalid queue name')

    def insert_message_queue(self, message):
        logger.info("Adding message: " + message)
        self.queue_client.send_message(message)

    def dequeue_message_queue(self):
        messages = self.queue_client.receive_messages()
        return messages

    def delete_processed_messages(self, messages):
        for message in messages:
            logger.info("Deleting message: " + message.content)
            self.queue_client.delete_message(message.id, message.pop_receipt)

    def delete_queue(self):
        logger.info("Deleting queue: " + self.queue_client.queue_name)
        self.queue_client.delete_queue()

    def queue_length(self):
        properties = self.queue_client.get_queue_properties()
        count = properties.approximate_message_count
        logger.info("Message count: " + str(count))
        return count
