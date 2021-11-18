from connect4 import models
from typing import List, Optional


def optional_int_to_player(player: Optional[int]) -> Optional[models.Player]:
    if player is None:
        return None
    return int_to_player(player)


def optional_player_to_int(player: Optional[models.Player]) -> Optional[int]:
    if player is None:
        return None
    return player_to_int(player)


def int_to_player(player: int) -> models.Player:
    return {
        1: models.Player.ONE,
        2: models.Player.TWO,
    }[player]


def player_to_int(player: models.Player) -> int:
    return int(player)


def int_to_tile(tile: int) -> models.Tile:
    return {
        0: models.Tile.EMPTY,
        1: models.Tile.ONE,
        2: models.Tile.TWO,
    }[tile]


def player_to_tile(player: models.Player) -> models.Tile:
    return {
        models.Player.ONE: models.Tile.ONE,
        models.Player.TWO: models.Tile.TWO,
    }[player]


def tile_to_int(tile: models.Tile) -> int:
    return int(tile)


def str_to_board(board: str) -> List[List[models.Tile]]:
    columns = []
    for x in range(7):
        column = []
        for y in range(6):
            tile = int(board[x * 6 + y])
            column.append(int_to_tile(tile))
        columns.append(column)
    return columns


def board_to_str(board: List[List[models.Tile]]) -> str:
    result = ""
    for x in range(7):
        for y in range(6):
            result += str(int(board[x][y]))
    return result
