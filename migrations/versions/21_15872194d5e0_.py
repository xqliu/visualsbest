# coding=utf-8
"""在作品主推列表中增加名称字段和标题显示的css class

Revision ID: 15872194d5e0
Revises: 399e358e81fb
Create Date: 2015-11-23 22:49:58.280431

"""

# revision identifiers, used by Alembic.
revision = '15872194d5e0'
down_revision = '399e358e81fb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('photo_omnibus', sa.Column('name', sa.String(length=32), nullable=True))
    op.execute('UPDATE "photo_omnibus" SET "name" = \'\'')
    op.alter_column('photo_omnibus', 'name', nullable=False)
    op.add_column('photo_omnibus', sa.Column('title_class', sa.String(length=16), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('photo_omnibus', 'title_class')
    op.drop_column('photo_omnibus', 'name')
    ### end Alembic commands ###
