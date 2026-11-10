"""remove redundant user unique indexes

Revision ID: 75d4c1e0e15f
Revises: 49eb72aabe9d
Create Date: 2026-11-10 02:40:16.105392

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '75d4c1e0e15f'
down_revision: Union[str, Sequence[str], None] = '49eb72aabe9d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index("ix_users_email", table_name="users")



def downgrade() -> None:
    op.create_unique_constraint(
        "users_username_key",
        "users",
        ["username"]
    )
