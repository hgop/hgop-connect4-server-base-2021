from typing import Any, Tuple
from connect4 import converter
from connect4 import database
from connect4 import exceptions
from connect4 import game_logic
from connect4 import models
from connect4 import tokens


def index() -> Tuple[str, int]:
    return "Game Server", 200


def status() -> Tuple[str, int]:
    return "Running", 200


def create_game(json: Any) -> Tuple[dict, int]:
    models.CreateGameRequest(json)

    gameId = tokens.generate_token(32)

    gameActive = True
    gameWinner = None
    gameActivePlayer = 1
    gameBoard = "000000" + "000000" + "000000" + \
        "000000" + "000000" + "000000" + "000000"

    game = database.create_game(
        gameId=gameId,
        active=gameActive,
        winner=gameWinner,
        activePlayer=gameActivePlayer,
        board=gameBoard,
    )

    playerId = tokens.generate_token(32)
    playerNumber = 1

    database.add_player_to_game(
        playerId=playerId,
        gameId=gameId,
        number=playerNumber)

    return models.CreateGameResponse(
        gameId=gameId,
        active=gameActive,
        playerId=playerId,
        winner=converter.optional_int_to_player(gameWinner),
        playerNumber=converter.int_to_player(playerNumber),
        activePlayer=converter.int_to_player(gameActivePlayer),
        playerCount=1,
        board=converter.str_to_board(gameBoard),
    ).to_json(), 201


def join_game(json: Any) -> Tuple[dict, int]:
    req = models.JoinGameRequest(json)

    game = database.get_game(req.gameId)
    if game is None:
        raise exceptions.ApiException("Game not found", 404)

    players = database.get_players(req.gameId)
    if len(players) >= 2:
        raise exceptions.ApiException("Game is full", 404)

    playerId = tokens.generate_token(32)
    playerNumber = len(players) + 1

    database.add_player_to_game(
        playerId=playerId,
        gameId=game.gameId,
        number=playerNumber)

    return models.JoinGameResponse(
        gameId=game.gameId,
        active=game.active,
        playerId=playerId,
        winner=converter.optional_int_to_player(game.winner),
        playerNumber=converter.int_to_player(playerNumber),
        activePlayer=converter.int_to_player(game.activePlayer),
        playerCount=2,
        board=converter.str_to_board(game.board),
    ).to_json(), 202


def get_game(gameId: str, playerId: str) -> Tuple[dict, int]:
    game = database.get_game(gameId)
    if game is None:
        raise exceptions.ApiException("Game not found", 404)

    player = database.get_player(playerId)
    if player is None:
        raise exceptions.ApiException("Player not found", 404)

    players = database.get_players(gameId)

    return models.GetGameResponse(
        gameId=game.gameId,
        active=game.active,
        playerId=player.playerId,
        winner=converter.optional_int_to_player(game.winner),
        playerNumber=converter.int_to_player(player.number),
        activePlayer=converter.int_to_player(game.activePlayer),
        playerCount=len(players),
        board=converter.str_to_board(game.board),
    ).to_json(), 200


def make_move(json: Any) -> Tuple[dict, int]:
    req = models.MakeMoveRequest(json)

    game = database.get_game(req.gameId)
    if game is None:
        raise exceptions.ApiException("Game not found", 404)

    player = database.get_player(req.playerId)
    if player is None:
        raise exceptions.ApiException("Player not found", 404)

    players = database.get_players(req.gameId)
    if len(players) < 2:
        raise exceptions.ApiException("Game not started", 412)

    if game.activePlayer != player.number:
        raise exceptions.ApiException("Not your turn", 403)

    state = models.Game(
        gameId=game.gameId,
        active=game.active,
        winner=converter.optional_int_to_player(game.winner),
        activePlayer=converter.int_to_player(game.activePlayer),
        board=converter.str_to_board(game.board),
    )

    if not state.active:
        raise exceptions.ApiException("Game is over", 403)

    if game_logic.is_column_full(state, req.column):
        raise exceptions.ApiException("Column is full", 409)

    state = game_logic.make_move(state, req.column)

    database.update_game(
        gameId=state.gameId,
        active=state.active,
        winner=converter.optional_player_to_int(state.winner),
        activePlayer=int(state.activePlayer),
        board=converter.board_to_str(state.board),
    )

    return models.MakeMoveResponse(
        gameId=game.gameId,
        active=state.active,
        playerId=player.playerId,
        winner=state.winner,
        playerNumber=converter.int_to_player(player.number),
        activePlayer=state.activePlayer,
        playerCount=len(players),
        board=state.board,
    ).to_json(), 202
