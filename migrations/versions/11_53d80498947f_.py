# coding=utf-8
"""在image中增加public_id支持云端存储

Revision ID: 53d80498947f
Revises: 405a477bf820
Create Date: 2015-08-26 23:30:49.024250

"""

# revision identifiers, used by Alembic.
revision = '53d80498947f'
down_revision = '405a477bf820'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('image', sa.Column('public_id', sa.String(length=128), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('image', 'public_id')
    ### end Alembic commands ###
