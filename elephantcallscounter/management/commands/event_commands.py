import click
from flask import Blueprint

from elephantcallscounter.services.events_services import device_simulator

events = Blueprint("events", __name__)


@events.cli.command("device_simulator")
@click.argument("source_dir")
@click.argument("container_name")
@click.argument("queue_name")
@click.argument("dest_folder")
@click.pass_context
def device_simulator_command(
    context, source_dir, container_name, queue_name, dest_folder
):
    device_simulator(source_dir, container_name, queue_name, dest_folder)
