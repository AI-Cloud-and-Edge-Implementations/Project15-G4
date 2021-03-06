from datetime import datetime

from flask import Blueprint
from flask import render_template
from flask import request

from elephantcallscounter import db
from elephantcallscounter.application.persistence.models.elephants import Elephants
from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths
from elephantcallscounter.common.constants import LOCATION


template_folder_loc = join_paths([get_project_root(), 'app/templates'])

elephant_blueprint = Blueprint(
    'elephant',
    __name__,
    url_prefix = '/elephants',
    template_folder = template_folder_loc
)


@elephant_blueprint.route('/elephants_count/')
def elephant_counter():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    """
    TODO: Add time based aggregation:
            start_time >= Elephants.start_time
    ).filter(
        end_time <= Elephants.end_time
    """
    elephants = db.session.query(Elephants).all()
    print(start_time)
    print(end_time)
    elephant_output = [
        {elephant.device_id: elephant.number_of_elephants}
        for elephant in elephants
    ]
    location_data = [
        LOCATION[elephant.device_id]
        for elephant in elephants
    ]
    return render_template(
        'index.html',
        number_of_elephants = elephant_output,
        locations_data=location_data,
        labels = list(LOCATION.keys())
    )


@elephant_blueprint.route('/add_elephant_count/')
def add_elephant_count():
    start_time = datetime.strptime(
        request.args.get('start_time'), '%Y-%m-%d %H:%M:%S'
    )
    end_time = datetime.strptime(
        request.args.get('end_time'), '%Y-%m-%d %H:%M:%S'
    )
    new_elephant = Elephants(
        latitude = float(request.args.get('latitude')),
        longitude = float(request.args.get('longitude')),
        start_time = start_time,
        end_time = end_time,
        device_id = request.args.get('device_id'),
        number_of_elephants = int(request.args.get('number_of_elephants'))
    )
    db.session.add(new_elephant)
    db.session.commit()

    return {'message': 'new elephant added'}
