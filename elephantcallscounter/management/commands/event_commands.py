import click

from elephantcallscounter.services.events_services import send_to_iot


@click.group('events')
@click.pass_context
def events(context):
    pass


@events.command('send_data_to_device')
@click.pass_context
def send_data_to_device(context):
    send_to_iot()
