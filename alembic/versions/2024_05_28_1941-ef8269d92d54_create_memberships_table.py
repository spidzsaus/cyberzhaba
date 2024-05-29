# pylint: skip-file
"""Create memberships table

Revision ID: ef8269d92d54
Revises: 4883030f2a54
Create Date: 2024-05-28 19:41:48.623671+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef8269d92d54'
down_revision = '4883030f2a54'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('memberships',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.Column('guild', sa.Integer(), nullable=True),
    sa.Column('karma', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['guild'], ['guilds.discord_id'], ),
    sa.ForeignKeyConstraint(['user'], ['users.discord_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('memberships')
    # ### end Alembic commands ###
