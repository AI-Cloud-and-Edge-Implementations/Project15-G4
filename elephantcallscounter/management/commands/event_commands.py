import click

from elephantcallscounter.services.events_services import send_to_iot
from elephantcallscounter.services.events_services import receive_from_iot
from elephantcallscounter.utils.concurrency import run_in_parallel


@click.group('events')
@click.pass_context
def events(context):
    pass


@events.command('device_simulator')
@click.argument('container_name')
@click.argument('queue_name')
@click.argument('dest_folder')
@click.pass_context
def device_simulator(context, container_name, queue_name, dest_folder):
    run_in_parallel(
        lambda: send_to_iot(),
        lambda: receive_from_iot(container_name, queue_name, dest_folder)
    )
