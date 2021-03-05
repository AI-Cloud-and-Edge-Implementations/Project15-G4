from flask import Blueprint


def run_elephant_detection(file_path):
    print('file_path')


blob_blueprint = Blueprint(
    'blob_events',
    __name__,
    url_prefix = '/blobevents'
)


@blob_blueprint.route('/<string:file_path>', methods = ['GET', ])
def elephant_counter(file_path):
    run_elephant_detection(file_path)
