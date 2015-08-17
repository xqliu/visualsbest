# coding=utf-8
"""在 photo_collection中增加到Enum_Values的Category引用

Revision ID: 405a477bf820
Revises: 31ca7e7a871a
Create Date: 2015-08-17 23:42:20.257213

"""

# revision identifiers, used by Alembic.
revision = '405a477bf820'
down_revision = '31ca7e7a871a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('photo_collection',
                  sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'photo_collection', 'enum_values',
                          ['category_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('photo_collection', 'category_id')
    ### end Alembic commands ###
