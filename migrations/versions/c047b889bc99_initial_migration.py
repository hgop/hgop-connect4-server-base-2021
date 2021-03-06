"""Initial migration.

Revision ID: c047b889bc99
Revises: 
Create Date: 2021-11-18 17:56:29.243193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c047b889bc99'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('gameId', sa.String(length=32), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('winner', sa.Integer(), nullable=True),
    sa.Column('activePlayer', sa.Integer(), nullable=False),
    sa.Column('board', sa.String(length=42), nullable=False),
    sa.PrimaryKeyConstraint('gameId')
    )
    op.create_table('player',
    sa.Column('playerId', sa.String(length=32), nullable=False),
    sa.Column('gameId', sa.String(length=32), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['gameId'], ['game.gameId'], ),
    sa.PrimaryKeyConstraint('playerId'),
    sa.UniqueConstraint('gameId', 'number', name='_game_number_constraint')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('player')
    op.drop_table('game')
    # ### end Alembic commands ###
