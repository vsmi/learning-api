"""delete read from books

Revision ID: 388fd2a9717e
Revises: 184e407f1f31
Create Date: 2022-05-23 20:04:54.150737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '388fd2a9717e'
down_revision = '184e407f1f31'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('books', 'read')
    pass


def downgrade():
    op.add_column('books', sa.Column('read', sa.Boolean(), server_default=sa.text('True'), nullable=True))
    pass
