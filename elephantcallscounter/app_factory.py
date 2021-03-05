from flask import Flask
from flask_script import Manager
from flask_migrate import MigrateCommand

from elephantcallscounter import db
from elephantcallscounter import migrate
from elephantcallscounter.application.api.elephants_view import elephant_blueprint
from elephantcallscounter.application.api.blob_events import blob_blueprint
from elephantcallscounter.management.commands.data_import_commands import data_import
from elephantcallscounter.management.commands.data_analysis_commands import data_analysis
from elephantcallscounter.management.commands.data_processing_commands import data_processing
from elephantcallscounter.management.commands.demo_commands import demo
from elephantcallscounter.management.commands.event_commands import events
from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths


def create_app():
    app = Flask(__name__)
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///elephantscounter.sqlite3',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'DEBUG': True
    })
    db.init_app(app)
    migrate.init_app(
        app,
        db,
        MIGRATION_DIR = join_paths([get_project_root(), 'application/persistence/migrations'])
    )
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    app.register_blueprint(data_analysis)
    app.register_blueprint(data_import)
    app.register_blueprint(data_processing)
    app.register_blueprint(demo)
    app.register_blueprint(events)
    # api blueprints
    app.register_blueprint(elephant_blueprint)
    app.register_blueprint(blob_blueprint)

    return app
