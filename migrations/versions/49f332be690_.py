# coding=utf-8
"""在用户profile中增加其每日报价

Revision ID: 49f332be690
Revises: 4efe4244247d
Create Date: 2015-09-01 09:27:32.042990

"""

# revision identifiers, used by Alembic.
revision = '49f332be690'
down_revision = '4efe4244247d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users',
                  sa.Column('daily_price', sa.Numeric(precision=8, scale=2, decimal_return_scale=2), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'daily_price')
    ### end Alembic commands ###
