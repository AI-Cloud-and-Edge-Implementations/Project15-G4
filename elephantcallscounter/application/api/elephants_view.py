from datetime import datetime

from flask import Blueprint
from flask import current_app
from flask import render_template
from flask import request
from flask_googlemaps import Map
from flask_googlemaps import GoogleMaps

from elephantcallscounter import db
from elephantcallscounter.application.persistence.models.elephants import Elephants
from elephantcallscounter.config import env
from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths


template_folder_loc = join_paths([get_project_root(), 'app/templates'])

elephant_blueprint = Blueprint(
    'elephant',
    __name__,
    url_prefix = '/elephants',
    template_folder = template_folder_loc
)


GoogleMaps(current_app, key = env.GOOGLE_API_KEY)


@elephant_blueprint.route('/elephants_count/')
def elephant_counter():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    elephants = db.session.query(Elephants).filter(
        start_time >= Elephants.start_time
    ).filter(
        end_time <= Elephants.end_time
    ).all()
    print(start_time)
    print(end_time)
    elephant_output = [
        {elephant.device_id: elephant.number_of_elephants}
        for elephant in elephants
    ]

    return render_template(
        'index.html',
        number_of_elephants = elephant_output,
        locations_data=[
            {'lat': 0.0236, 'lng': 37.9062},
            {'lat': 0.08, 'lng': 38.9062},
            {'lat': 1.5, 'lng': 39.9062}
        ],
        labels = ['nn01', 'nn02', 'nn03']
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
        device_id = int(request.args.get('device_id')),
        number_of_elephants = int(request.args.get('number_of_elephants'))
    )
    db.session.add(new_elephant)
    db.session.commit()

    return {'message': 'new elephant added'}
