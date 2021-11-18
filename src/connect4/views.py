from flask import Flask, request
from typing import Any, Callable, Tuple
from connect4 import exceptions
from connect4 import app_logic


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


def register(app: Flask):
    @app.route("/", methods=["GET"])
    def index() -> Tuple[str, int]:
        return call_wrapper(app_logic.index)

    @app.route("/status", methods=["GET"])
    def status() -> Tuple[str, int]:
        return call_wrapper(app_logic.status)

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
