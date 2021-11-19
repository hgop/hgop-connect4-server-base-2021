from typing import List, Optional
from flask_sqlalchemy import SQLAlchemy  # type: ignore

db = SQLAlchemy()


class GameEntity(db.Model):  # type: ignore
    __tablename__ = 'game'

    gameId = db.Column(db.String(32), primary_key=True)
    active = db.Column(db.Boolean, nullable=False)
    winner = db.Column(db.Integer, nullable=True)
    activePlayer = db.Column(db.Integer, nullable=False)
    board = db.Column(db.String(42), nullable=False)

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


class PlayerEntity(db.Model):  # type: ignore
    __tablename__ = 'player'

    playerId = db.Column(db.String(32), primary_key=True)
    gameId = db.Column(
        db.String(32),
        db.ForeignKey('game.gameId'),
        nullable=False)
    number = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint(
            'gameId',
            'number',
            name='_game_number_constraint'),
    )

    def __init__(self, playerId: str, gameId: str, number: int) -> None:
        self.playerId = playerId
        self.gameId = gameId
        self.number = number


def create_game(
        gameId: str,
        active: bool,
        winner: Optional[int],
        activePlayer: int,
        board: str) -> GameEntity:
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
    return PlayerEntity.query.get(playerId)


def update_game(
        gameId: str,
        active: bool,
        winner: Optional[int],
        activePlayer: int,
        board: str) -> None:
    game = GameEntity.query.get(gameId)
    game.active = active
    game.winner = winner,
    game.activePlayer = activePlayer
    game.board = board
    db.session.commit()
