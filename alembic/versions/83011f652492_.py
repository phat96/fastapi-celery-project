"""empty message

Revision ID: 83011f652492
Revises: 6feca6ca7293
Create Date: 2022-06-06 13:07:34.945738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83011f652492'
down_revision = '6feca6ca7293'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('members',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=128), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('avatar', sa.String(length=256), nullable=False),
    sa.Column('avatar_thumbnail', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('members')
    # ### end Alembic commands ###