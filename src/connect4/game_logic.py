from copy import deepcopy
from connect4 import converter
from connect4 import models


def make_move(game: models.Game, x: int) -> models.Game:
    result = models.Game(
        gameId=game.gameId,
        active=game.active,
        winner=game.winner,
        activePlayer=game.activePlayer,
        board=deepcopy(game.board),
    )

    for y in range(6):
        if result.board[x][y] == models.Tile.EMPTY:
            result.board[x][y] = converter.player_to_tile(result.activePlayer)
            if is_victory_move(result, x, y, result.activePlayer):
                result.winner = result.activePlayer
                result.active = False
            else:
                result.active = is_board_full(result) is False

            if result.activePlayer == models.Player.ONE:
                result.activePlayer = models.Player.TWO
            else:
                result.activePlayer = models.Player.ONE

            return result

    raise Exception("Row is full")


def is_victory_move(
        game: models.Game,
        x: int,
        y: int,
        player: models.Player) -> bool:
    return (
        is_victory_move_horizontal(game, x, y, player)
        or is_victory_move_vertical(game, x, y, player)
        or is_victory_move_diagonal(game, x, y, player)
    )


def is_victory_move_horizontal(
    game: models.Game, x: int, y: int, player: models.Player
) -> bool:
    # TODO
    return False


def is_victory_move_vertical(
    game: models.Game, x: int, y: int, player: models.Player
) -> bool:
    # TODO
    return False


def is_victory_move_diagonal(
    game: models.Game, x: int, y: int, player: models.Player
) -> bool:
    # TODO
    return False


def get_tile(game: models.Game, x: int, y: int) -> models.Tile:
    # TODO
    return models.Tile.EMPTY


def is_board_full(game: models.Game) -> bool:
    # TODO
    return False


def is_column_full(game: models.Game, column: int) -> bool:
    # TODO
    return False
