from flask import Flask
from flask_cors import CORS  # type: ignore
from flask_migrate import Migrate, MigrateCommand  # type: ignore
from flask_script import Manager  # type: ignore
from connect4 import config, database, views


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app)
    return app


if __name__ == "__main__":
    app = create_app()

    views.register(app)

    migrate = Migrate(app, database.db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    manager.run()
