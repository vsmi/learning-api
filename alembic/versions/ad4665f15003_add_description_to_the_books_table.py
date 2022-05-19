"""add description to the books table

Revision ID: ad4665f15003
Revises: c5889a541d8d
Create Date: 2022-05-18 10:02:33.932876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad4665f15003'
down_revision = 'c5889a541d8d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('books', sa.Column('description', sa.String(),  nullable=True))
    pass


def downgrade():
    op.drop_column('books', 'description')
    pass
