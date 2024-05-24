"""test

Revision ID: cf6b059cc3e5
Revises: 
Create Date: 2024-03-17 12:22:11.765944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf6b059cc3e5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False, autoincrement=True),
        sa.Column("title", sa.String, nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
