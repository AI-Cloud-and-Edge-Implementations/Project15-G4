import asyncio
from azure.eventhub.aio import EventHubConsumerClient

from elephantcallscounter.config import env
from elephantcallscounter.utils.file_utils import write_to_bin_file
from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths


async def on_event_batch(partition_context, events):
    for event in events:
        print("Received event from partition: {}.".format(partition_context.partition_id))
        print("Telemetry received: ", event.body_as_str())
        print("Properties (set by device): ", event.properties)
        print("System properties (set by IoT Hub): ", event.system_properties)
        write_to_bin_file(
            event,
            join_paths([get_project_root(), 'data/imported_data/' + event.message['file_name']])
        )

    await partition_context.update_checkpoint()


async def on_error(partition_context, error):
    # Put your code here. partition_context can be None in the on_error callback.
    if partition_context:
        print("An exception: {} occurred during receiving from Partition: {}.".format(
            partition_context.partition_id,
            error
        ))
    else:
        print("An exception: {} occurred during the load balance process.".format(error))


def consume_events():
    loop = asyncio.get_event_loop()
    client = EventHubConsumerClient.from_connection_string(
        conn_str = env.EVENTHUB_CONN_STRING,
        consumer_group = "$default"
    )
    try:
        loop.run_until_complete(
            client.receive_batch(on_event_batch = on_event_batch, on_error = on_error)
        )
    except KeyboardInterrupt:
        print("Receiving has stopped.")
    finally:
        loop.run_until_complete(client.close())
        loop.stop()
