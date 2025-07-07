"""add foreign-key to posts table

Revision ID: 452749a4e65e
Revises: 01113701db55
Create Date: 2025-07-02 08:24:00.031978

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '452749a4e65e'
down_revision: Union[str, Sequence[str], None] = '01113701db55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE") 

    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    """Downgrade schema."""
    pass
