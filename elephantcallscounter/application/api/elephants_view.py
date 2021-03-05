from datetime import datetime

from flask import Blueprint
from flask import render_template
from flask import request

from elephantcallscounter.app_factory import db
from elephantcallscounter.application.persistence.models.elephants import Elephants
from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths

template_folder_loc = join_paths([get_project_root(), 'app/templates'])

elephant_blueprint = Blueprint(
    'elephant',
    __name__,
    url_prefix = '/elephants',
    template_folder = template_folder_loc
)


@elephant_blueprint.route('/elephants_count/<string:start_time>/<string:end_time>/')
def elephant_counter(start_time, end_time):
    if request.method == 'GET':
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        elephants = db.session.query(Elephants).filter(
            start_time >= Elephants.start_time
        ).filter(
            end_time <= Elephants.end_time
        ).all()
        print(elephants)

    return render_template(join_paths([template_folder_loc, 'index.html']))
