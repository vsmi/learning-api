"""add book_status in books

Revision ID: 184e407f1f31
Revises: 7b189dfeccfb
Create Date: 2022-05-23 14:16:09.621453

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '184e407f1f31'
down_revision = 'ad4665f15003'
branch_labels = None
depends_on = None


def upgrade():
    book_status = postgresql.ENUM('in_progress', 'done', 'suspended', name='book_status')
    book_status.create(op.get_bind())
    op.add_column('books', sa.Column('status_of_book', sa.Enum('in_progress', 'done', 'suspended', name= 'book_status'),  nullable=True))
    pass


def downgrade():
    op.drop_column('books', 'status_of_book')
    book_status = postgresql.ENUM('in_progress', 'done', 'suspended', name='book_status')
    book_status.drop(op.get_bind())
    pass
