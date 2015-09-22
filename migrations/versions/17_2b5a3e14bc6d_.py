# coding=utf-8
"""在拍摄请求中删除字符类型的风格并增加列表类型的风格

Revision ID: 2b5a3e14bc6d
Revises: 5924eae17021
Create Date: 2015-09-22 22:35:56.140175

"""

# revision identifiers, used by Alembic.
revision = '2b5a3e14bc6d'
down_revision = '5924eae17021'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('request', 'style')
    op.add_column('request', sa.Column('style_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'request', 'enum_values', ['style_id'], ['id'])


def downgrade():
    op.drop_column('request', 'style_id')
    op.drop_column('request', 'category_id')
