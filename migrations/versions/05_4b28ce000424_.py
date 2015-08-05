# coding=utf-8
"""在用户表中增加更多的用户相关字段，生日性别个人介绍微信微博等

Revision ID: 4b28ce000424
Revises: 4260c45e0bd0
Create Date: 2015-08-05 22:06:59.846288

"""

# revision identifiers, used by Alembic.
revision = '4b28ce000424'
down_revision = '4260c45e0bd0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('birthday', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('gender', sa.String(length=8), nullable=True))
    op.add_column('users', sa.Column('introduce', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('wechat_account', sa.String(length=32), nullable=True))
    op.add_column('users', sa.Column('weibo_account', sa.String(length=32), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'weibo_account')
    op.drop_column('users', 'wechat_account')
    op.drop_column('users', 'introduce')
    op.drop_column('users', 'gender')
    op.drop_column('users', 'birthday')
    ### end Alembic commands ###