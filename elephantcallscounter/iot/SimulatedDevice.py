import time

from azure.iot.device import IoTHubDeviceClient, Message

from elephantcallscounter.config import env

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
CONNECTION_STRING = env.DEVICE_CONNECTION_STRING

# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
HUMIDITY = 60
MSG_TXT = '{{"file": "nn08c_20181118_000000.wav","duration": "7.696", "File_offset": "63209.6831", "uniqId": "nn08c_1199"}}'


def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client


def iothub_client_run_send_telemetry_events():
    try:
        client = iothub_client_init()
        print("IoT Hub device sending periodic messages, press Ctrl-C to exit")

        while True:
            msg_txt_formatted = MSG_TXT.format()
            message = Message(msg_txt_formatted)

            print("Sending message: {}".format(message))
            client.send_message(message)
            print("Message successfully sent")
            time.sleep(1)

    except KeyboardInterrupt:
        print("IoTHubClient sample stopped")
