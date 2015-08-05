# coding=utf-8
"""在主推模板中增加名称和模板文件路径字段, 增加订单和用户表相关字段

Revision ID: 4260c45e0bd0
Revises: 38ef93735a7d
Create Date: 2015-08-01 14:08:22.866739

"""

# revision identifiers, used by Alembic.
revision = '4260c45e0bd0'
down_revision = '38ef93735a7d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('omnibus_template', sa.Column('path', sa.String(length=128),
                                                nullable=False))
    op.add_column('omnibus_template', sa.Column('name', sa.String(length=32),
                                                nullable=False))
    op.add_column('order', sa.Column('amount',
                                     sa.Numeric(precision=8, scale=2,
                                                decimal_return_scale=2),
                                     nullable=False))
    op.add_column('users', sa.Column('mobile_phone', sa.String(length=16),
                                     nullable=True))
    op.execute('update "users" set mobile_phone = \'DUMMY_MP\'')
    op.alter_column('users', 'mobile_phone', nullable=False)
    op.add_column('users', sa.Column('qq_number', sa.String(length=16),
                                     nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'qq_number')
    op.drop_column('users', 'mobile_phone')
    op.drop_column('order', 'amount')
    op.drop_column('omnibus_template', 'name')
    op.drop_column('omnibus_template', 'path')
    ### end Alembic commands ###
