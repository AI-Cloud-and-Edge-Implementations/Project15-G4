# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Adapted from
# https://github.com/Azure/azure-iot-sdk-python/blob/master/azure-iot-device/samples/async-hub-scenarios/send_message.py

import os
import json
import asyncio
import uuid
import time
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

messages_to_send = 10


async def main():
    # The connection string for a device should never be stored in code. For the sake of simplicity we're using an environment variable here.
    conn_str = "<DEVICE_CONN_STRING>"

    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the client.
    await device_client.connect()

    # Get the list of all files in the spectrograms_boxed directory
    # read the content and send it to IoTHub as a message

    async def send_spectrogram():
        sleepInterval = 5

    path = "./spectrograms_boxed"
    spectrogram_list = os.listdir(path)
    while True:
        for f in spectrogram_list:
    # open file
    file = open(path + '/' + f, "rb")
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
    await asyncio.sleep(sleepInterval)

    # Define behavior for halting the application
    def stdin_listener():
        while True:
            selection = input('Press Q to quit\n')

    if selection == 'Q' or selection == 'q':
        print('Quitting...')
        break

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
