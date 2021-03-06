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

    json_data = { # for testing
        'user' : {
            'x' : 37.50611,
            'y' : 127.0616346
        },
        'devices' : [
            {
                'id' : '0001',
                'x' : 37.5077121,
                'y' : 127.0624397,
                'data' : 'something'
            }
        ]
    }
    devices_data = {}  # dict to store data of devices
    devices_location = {}  # dict to store coordinates of devices

    user_location = (json_data['user']['x'], json_data['user']['y'])
    # json example : { 'user' : { 'x' : '300' , 'y' : '300' } }
    # get user_location from json & store as turple (x, y)

    devices_data[str(json_data['devices'][0]['id'])] = (
        json_data['devices'][0]['data']
    )

    devices_location[str(json_data['devices'][0]['id'])] = (
        json_data['devices'][0]['x'],
        json_data['devices'][0]['y']
    )
    # json example : { 'devices' : { 'id' : '0001', x' : '500', 'y' : '500' }, { ... } }
    # get device_location from json & store turple (x, y) in dictionary with device id as key
    # use for statements or something to get more locations from more devices

    circle = { # draw circle on map (user_location as center)
        'stroke_color': '#0000FF',
        'stroke_opacity': .5,
        'stroke_weight': 5,
        # line(stroke) style
        'fill_color': '#FFFFFF',
        'fill_opacity': .2,
        # fill style
        'center': { # set circle to user_location
            'lat': user_location[0],
            'lng': user_location[1]
        },
        'radius': 500 # circle size (50 meters)
    }

    map = Map(
        identifier = "map", varname = "map",
        # set identifier, varname
        lat = user_location[0], lng = user_location[1],
        # set map base to user_location
        zoom = 15, # set zoomlevel
        markers = [
            {
                'lat': devices_location['0001'][0],
                'lng': devices_location['0001'][1],
                'infobox': devices_data['0001']
            }
        ],
        # set markers to location of devices
        circles = [circle] # pass circles
    )

    return render_template(
        'index.html',
        map=map,
        locations_data=[
            {'lat': 0.0236, 'lng': 37.9062},
            {'lat': 0.08, 'lng': 38.9062},
            {'lat': 1.5, 'lng': 39.9062}
        ],
        labels = [0, 1, 2]
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
