"""nullify all message edit activity tracking events

Revision ID: 3a8e7ff77c93
Revises: 35738600e80c
Create Date: 2025-02-20 20:19:35.191108+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a8e7ff77c93'
down_revision = '35738600e80c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("UPDATE users SET last_activity = NULL, last_activity_type = NULL \
WHERE last_activity_type LIKE '%message edited%'")
    op.execute("UPDATE memberships SET last_activity = NULL, last_activity_type = NULL \
WHERE last_activity_type LIKE '%message edited%'")


def downgrade() -> None:
    pass
