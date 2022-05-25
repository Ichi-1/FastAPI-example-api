"""empty message

Revision ID: 2ff5e5858fa0
Revises: 
Create Date: 2022-05-25 17:36:30.622779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ff5e5858fa0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users', 
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_ad', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('phone_number', sa.String, nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('is_published', sa.Boolean(), default=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
    )
    op.create_foreign_key(
        'post_users_fk', 
        source_table='posts', 
        referent_table='users', 
        local_cols=['owner_id'], 
        remote_cols=['id'], 
        ondelete='CASCADE'
    )

    pass


def downgrade():
    op.drop_table('users')
    op.drop_table('posts')
    pass
