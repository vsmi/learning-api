"""add books table

Revision ID: 8462f9a1fcd7
Revises: 6da4eac585c9
Create Date: 2022-03-07 11:20:16.953090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8462f9a1fcd7'
down_revision = '6da4eac585c9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('books',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('author', sa.String(), nullable=True),
                    sa.Column('rating', sa.Float(), nullable=True),
                    sa.Column('read', sa.Boolean(), server_default=sa.text('True'), nullable=True),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )

    pass


def downgrade():
    op.drop_table('books')
    pass
