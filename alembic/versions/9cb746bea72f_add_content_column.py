"""add content column

Revision ID: 9cb746bea72f
Revises: cf6b059cc3e5
Create Date: 2024-03-17 12:28:53.519183

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cb746bea72f'
down_revision: Union[str, None] = 'cf6b059cc3e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    pass


def downgrade() -> None:
    pass
