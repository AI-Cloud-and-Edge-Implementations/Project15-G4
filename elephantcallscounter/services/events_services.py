import asyncio
from elephantcallscounter.iot.iot_handler import write_to_hub


def send_to_iot():
    asyncio.run(write_to_hub())
