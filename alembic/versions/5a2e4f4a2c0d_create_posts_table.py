"""create posts table

Revision ID: 5a2e4f4a2c0d
Revises: 
Create Date: 2025-07-01 09:47:05.985373

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a2e4f4a2c0d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:#handles the changes
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    """Upgrade schema."""
    pass


def downgrade() -> None:#handles rolling the changes back
    op.derop_table('posts')
    """Downgrade schema."""
    pass
