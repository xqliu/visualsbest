# coding=utf-8
"""删除用户状态字段，改为根据confirmed_at设定的动态属性

Revision ID: 499f3dd6151c
Revises: 4260c45e0bd0
Create Date: 2015-08-04 11:06:31.284919

"""

# revision identifiers, used by Alembic.
revision = '499f3dd6151c'
down_revision = '4260c45e0bd0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'user_status_id_fkey', 'user', type_='foreignkey')
    op.drop_column('user', 'status_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('status_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key(u'user_status_id_fkey', 'user', 'enum_values', ['status_id'], ['id'])
    ### end Alembic commands ###