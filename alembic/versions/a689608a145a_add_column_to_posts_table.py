"""add column to posts table

Revision ID: a689608a145a
Revises: 5a2e4f4a2c0d
Create Date: 2025-07-01 10:07:23.498707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a689608a145a'
down_revision: Union[str, Sequence[str], None] = '5a2e4f4a2c0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    """Downgrade schema."""
    pass
