from connect4.app import db, GameEntity, PlayerEntity
from typing import List, Optional

def create_game(
    gameId: str, active: bool, winner: Optional[int], activePlayer: int, board: str
) -> GameEntity:
    game = GameEntity(
        gameId=gameId,
        active=active,
        winner=winner,
        activePlayer=activePlayer,
        board=board
    )
    db.session.add(game)
    db.session.commit()
    return game


def add_player_to_game(playerId: str, gameId: str, number: int) -> None:
    db.session.add(PlayerEntity(
        playerId=playerId,
        gameId=gameId,
        number=number
    ))
    db.session.commit()


def get_game(gameId: str) -> Optional[GameEntity]:
    return GameEntity.query.get(gameId)


def get_players(gameId: str) -> List[PlayerEntity]:
    return PlayerEntity.query.filter_by(gameId=gameId).all()


def get_player(playerId: str) -> Optional[PlayerEntity]:
    return PlayerEntity.query.get(playerId=playerId)


def update_game(
    gameId: str, active: bool, winner: Optional[int], activePlayer: int, board: str
) -> None:
    game = GameEntity.query.get(gameId)
    game.active = active
    game.winner = winner,
    game.activePlayer = activePlayer
    game.board = board
    db.session.commit()