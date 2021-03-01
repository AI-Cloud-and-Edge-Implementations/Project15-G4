import os
import json
import asyncio
import uuid
import time
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

from elephantcallscounter.config import env
from elephantcallscounter.utils.path_utils import join_paths


async def write_to_hub(source_path, list_of_files):
    conn_str = env.IOT_HUB_CONN_STRING

    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the client.
    await device_client.connect()

    async def send_spectrogram():
        sleep_interval = 5
        while True:
            for f in list_of_files:
                file = open(join_paths([source_path, f]), "rb")
                file_content = file.read()
                file.close()
                payload = json.dumps({
                    'capturedate': time.time(),
                    'filename': f,
                    'spectrogram': str(file_content)
                })
                msg = Message(payload)
                msg.message_id = uuid.uuid4()
                msg.content_encoding = "utf-8"
                msg.content_type = "application/json"
                await device_client.send_message(msg)
                print("done sending file " + str(f))
                print(payload)
                await asyncio.sleep(sleep_interval)

    # Define behavior for halting the application
    def stdin_listener():
        while True:
            try:
                selection = input()
                if selection == 'Q' or selection == 'q':
                    print('Quitting...')
                    break
            except EOFError as e:
                time.sleep(10000)

    tasks = asyncio.gather(
        send_spectrogram()
    )

    # Run the stdin listener in the event loop
    loop = asyncio.get_running_loop()
    user_finished = loop.run_in_executor(None, stdin_listener)

    # Wait for user to indicate they are done listening for method calls
    await user_finished

    # Cancel tasks
    tasks.add_done_callback(lambda r: r.exception())
    tasks.cancel()
    await device_client.disconnect()
