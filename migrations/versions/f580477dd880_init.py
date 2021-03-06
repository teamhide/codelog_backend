"""init

Revision ID: f580477dd880
Revises: 
Create Date: 2020-01-27 02:26:30.675203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f580477dd880'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Unicode(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('email', sa.Unicode(length=255), nullable=True),
    sa.Column('nickname', sa.Unicode(length=255), nullable=True),
    sa.Column('avatar_url', sa.Unicode(length=255), nullable=True),
    sa.Column('login_type', sa.Unicode(length=20), nullable=False),
    sa.Column('access_token', sa.Unicode(length=255), nullable=False),
    sa.Column('refresh_token', sa.Unicode(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feeds',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('image', sa.Unicode(length=255), nullable=True),
    sa.Column('title', sa.Unicode(length=255), nullable=True),
    sa.Column('description', sa.Unicode(length=255), nullable=True),
    sa.Column('url', sa.Unicode(length=1000), nullable=False),
    sa.Column('is_private', sa.Boolean(), nullable=True),
    sa.Column('is_read', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feed_tag',
    sa.Column('feed_id', sa.BigInteger(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['feed_id'], ['feeds.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feed_tag')
    op.drop_table('feeds')
    op.drop_table('users')
    op.drop_table('tags')
    # ### end Alembic commands ###
