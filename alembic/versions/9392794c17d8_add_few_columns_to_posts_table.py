"""add few columns to posts table

Revision ID: 9392794c17d8
Revises: 452749a4e65e
Create Date: 2025-07-02 08:55:46.005052

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9392794c17d8'
down_revision: Union[str, Sequence[str], None] = '452749a4e65e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at',sa.TIMESTAMP(timezone=True), nullable=False, server_dafault=sa.text('NOW()')))
    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')

    """Downgrade schema."""
    pass
