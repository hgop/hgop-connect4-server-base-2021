from flask import Flask
from flask_cors import CORS  # type: ignore
from flask_migrate import Migrate  # type: ignore
from connect4 import config, database, views

app = Flask(__name__)
app.config.from_object(config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

migrate = Migrate(app, database.db)
database.db.init_app(app)


if __name__ == "__main__":
    views.register(app)
    app.run(host=config.HOST, port=config.PORT)
