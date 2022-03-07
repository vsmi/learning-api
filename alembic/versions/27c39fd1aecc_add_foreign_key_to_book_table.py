"""add foreign key to book table

Revision ID: 27c39fd1aecc
Revises: 8462f9a1fcd7
Create Date: 2022-03-07 11:25:14.645348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27c39fd1aecc'
down_revision = '8462f9a1fcd7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('books', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('books_users_fk', source_table="books", referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constrant('books_users_fk', table_name="books")
    op.drop_column('books', 'owner_id')
    pass

