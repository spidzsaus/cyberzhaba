# pylint: skip-file
"""THE GREAT KARMA MIGRATION

Revision ID: eb641f2b605c
Revises: ef8269d92d54
Create Date: 2024-05-28 19:42:20.074145+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb641f2b605c'
down_revision = 'ef8269d92d54'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("INSERT INTO guilds (discord_id) VALUES ('450920216550047744')")
    op.execute("INSERT INTO memberships (user, guild, karma) \
SELECT discord_id, '450920216550047744', karma FROM users")

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'karma')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('karma', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###
