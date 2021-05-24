import logging

from flask import Flask
from flask_migrate import MigrateCommand
from flask_script import Manager

from elephantcallscounter import db, migrate
from elephantcallscounter.application.api.blob_events import blob_blueprint
from elephantcallscounter.application.api.elephants_view import \
    elephant_blueprint
from elephantcallscounter.management.commands.data_analysis_commands import \
    data_analysis
from elephantcallscounter.management.commands.data_import_commands import \
    data_import
from elephantcallscounter.management.commands.data_processing_commands import \
    data_processing
from elephantcallscounter.management.commands.event_commands import events
from elephantcallscounter.management.commands.pipeline_commands import demo
from elephantcallscounter.utils.path_utils import get_project_root, join_paths


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Set the logging level for all azure-* libraries
    # Disable Logger for Azure Event Hubs
    logging.getLogger("uamqp").setLevel(
        logging.CRITICAL
    )  # Low level uAMQP are logged only for critical
    logging.getLogger("azure").setLevel(
        logging.CRITICAL
    )  # All azure clients are logged only for critical

    # create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)


def create_app():
    setup_logging()
    app = Flask(__name__, template_folder="application/templates/")
    app.config.update(
        {
            "SQLALCHEMY_DATABASE_URI": "sqlite:///elephantscounter.sqlite3",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "DEBUG": True,
        }
    )
    db.init_app(app)
    migrate.init_app(
        app,
        db,
        MIGRATION_DIR=join_paths(
            [get_project_root(), "application/persistence/migrations"]
        ),
    )
    manager = Manager(app)
    manager.add_command("db", MigrateCommand)
    app.register_blueprint(data_analysis)
    app.register_blueprint(data_import)
    app.register_blueprint(data_processing)
    app.register_blueprint(demo)
    app.register_blueprint(events)
    # api blueprints
    app.register_blueprint(elephant_blueprint)
    app.register_blueprint(blob_blueprint)

    return app
