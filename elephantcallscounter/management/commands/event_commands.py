import click

from elephantcallscounter.services.events_services import send_to_iot
from elephantcallscounter.services.events_services import receive_from_iot
from elephantcallscounter.utils.concurrency import run_in_parallel


@click.group('events')
@click.pass_context
def events(context):
    pass


@events.command('device_simulator')
@click.pass_context
def device_simulator(context):
    run_in_parallel(send_to_iot, receive_from_iot)
