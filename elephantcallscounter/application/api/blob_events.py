from flask import Blueprint
from elephantcallscounter.management.commands.pipeline_commands import run_demo

blob_blueprint = Blueprint(
    'blob_events',
    __name__,
    url_prefix = '/blobevents'
)


@blob_blueprint.route('/run_pipeline/<string:file_path>', methods = ['GET'])
def run_processing(file_path):
    run_demo(file_path)

    return
