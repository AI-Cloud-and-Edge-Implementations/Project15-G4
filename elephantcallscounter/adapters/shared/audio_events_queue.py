from azure.core.exceptions import HttpResponseError, ResourceExistsError
from azure.storage.queue import QueueClient, BinaryBase64EncodePolicy, BinaryBase64DecodePolicy

from elephantcallscounter.config import env


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
        print("Creating queue: " + self.queue_name)
        # Create the queue
        try:
            self.queue_client.create_queue()
        except ResourceExistsError:
            print('Queue {} already exists!'.format(self.queue_name))
        except HttpResponseError:
            print('Invalid queue name')

    def insert_message_queue(self, message):
        print("Adding message: " + message)
        self.queue_client.send_message(message)

    def dequeue_message_queue(self):
        messages = self.queue_client.receive_messages()
        return messages

    def delete_processed_messages(self, messages):
        for message in messages:
            print("Deleting message: " + message.content)
            self.queue_client.delete_message(message.id, message.pop_receipt)

    def delete_queue(self):
        print("Deleting queue: " + self.queue_client.queue_name)
        self.queue_client.delete_queue()

    def queue_length(self):
        properties = self.queue_client.get_queue_properties()
        count = properties.approximate_message_count
        print("Message count: " + str(count))
        return count
