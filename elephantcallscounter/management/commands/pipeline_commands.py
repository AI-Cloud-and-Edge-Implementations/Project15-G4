import click
from flask import Blueprint

from elephantcallscounter.services.pipeline_services import pipeline_run

demo = Blueprint('demo', __name__)


@demo.cli.command('run_demo')
@demo.cli.argument('file_path')
@click.pass_context
def run_demo(context, file_path):
    pipeline_run(file_path = file_path)
