"""empty message

Revision ID: 6ae6bb7f5ddc
Revises: af5307a8e08d
Create Date: 2017-08-29 16:14:45.501384

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy import Text


# revision identifiers, used by Alembic.
revision = '6ae6bb7f5ddc'
down_revision = 'af5307a8e08d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('link', 'token_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('link', 'url',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('token', 'identity',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('token', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('user', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('token', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('token', 'identity',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('link', 'url',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('link', 'token_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###