import click

from elephantcallscounter.services.events_services import send_to_iot
from elephantcallscounter.services.events_services import receive_from_iot
from elephantcallscounter.utils.concurrency import run_in_parallel


@click.group('events')
@click.pass_context
def events(context):
    pass


@events.command('send_data_to_device')
@click.pass_context
def send_data_to_device(context):
    run_in_parallel(send_to_iot, receive_from_iot)


@events.command('full_cycle')
@click.pass_context
def full_cycle(context):
    full_cycle()
