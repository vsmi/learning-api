"""add users table

Revision ID: 6da4eac585c9
Revises: 
Create Date: 2022-03-07 11:12:34.733289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6da4eac585c9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
