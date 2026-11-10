"""remove duplicate username const

Revision ID: 49eb72aabe9d
Revises: a527a20ed9fb
Create Date: 2026-11-10 02:34:37.687701

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49eb72aabe9d'
down_revision: Union[str, Sequence[str], None] = 'a527a20ed9fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "users_username_key",
        "users",
        type_="unique"
    )


def downgrade() -> None:
    op.create_unique_constraint(
        "users_username_key",
        "users",
        ["username"]
    )
