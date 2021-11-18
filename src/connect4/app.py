from connect4 import app_logic
from connect4 import config
from connect4 import exceptions
from datetime import datetime
from flask import Flask, request
from flask_cors import CORS # type: ignore
from flask_migrate import Migrate, MigrateCommand # type: ignore
from flask_script import Manager # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from typing import Any, Callable, Optional, Tuple

app = Flask(__name__)
app.config.from_object(config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class GameEntity(db.Model): # type: ignore
    __tablename__ = 'game'

    gameId = db.Column(db.String(32), primary_key=True)
    active = db.Column(db.Boolean, nullable=False)
    winner = db.Column(db.Integer, nullable=True)
    activePlayer = db.Column(db.Integer, nullable=False)
    board = db.Column(db.String(42), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(
        self,
        gameId: str,
        active: bool,
        winner: Optional[int],
        activePlayer: int,
        board: str,
    ) -> None:
        self.gameId = gameId
        self.active = active
        self.winner = winner
        self.activePlayer = activePlayer
        self.board = board


class PlayerEntity(db.Model): # type: ignore
    __tablename__ = 'player'

    playerId = db.Column(db.String(32), primary_key=True)
    gameId = db.Column(db.String(32), db.ForeignKey('game.gameId'), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('gameId', 'number', name='_game_number_constraint'),)

    def __init__(self, playerId: str, gameId: str, number: int) -> None:
        self.playerId = playerId
        self.gameId = gameId
        self.number = number

def call_wrapper(action: Callable[[], Tuple[Any, int]]) -> Tuple[Any, int]:
    try:
        return action()
    except exceptions.ApiException as ex:
        print(ex)
        return {
            "error": ex.message,
        }, ex.status_code
    except Exception as ex:
        print(ex)
        return {
            "error": "Internal Server Error",
        }, 500


@app.route("/", methods=["GET"])
def index() -> Tuple[str, int]:
    return call_wrapper(
        lambda: app_logic.index()
    )


@app.route("/status", methods=["GET"])
def status() -> Tuple[str, int]:
    return call_wrapper(
        lambda: app_logic.status()
    )


@app.route("/create_game", methods=["POST"])
def create_game() -> Tuple[dict, int]:
    return call_wrapper(
        lambda: app_logic.create_game(request.json)
    )

@app.route("/join_game", methods=["POST"])
def join_game() -> Tuple[dict, int]:
    return call_wrapper(
        lambda: app_logic.join_game(request.json)
    )

@app.route("/get_game", methods=["GET"])
def get_game() -> Tuple[dict, int]:
    gameId = request.args.get("gameId", "")
    playerId = request.args.get("playerId", "")
    return call_wrapper(
        lambda: app_logic.get_game(gameId, playerId)
    )


@app.route("/make_move", methods=["POST"])
def make_move() -> Tuple[dict, int]:
    return call_wrapper(
        lambda: app_logic.make_move(request.json)
    )


if __name__ == "__main__":
    manager.run()