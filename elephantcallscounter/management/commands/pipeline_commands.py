import click
from flask import Blueprint

from elephantcallscounter.services.pipeline_services import pipeline_run

demo = Blueprint('demo', __name__)


@demo.cli.command('run_demo')
@click.argument('folder_path')
@click.pass_context
def run_demo(context, folder_path):
    pipeline_run(folder_path, csv_file_path = 'data/labels/spec_images_labels.csv')
