# coding=utf-8
"""在作品集中增加名字、分类、风格、日期、简介等，作品分类中增加名称

Revision ID: 33eb76c3c32f
Revises: 4b28ce000424
Create Date: 2015-08-07 22:33:02.259836

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '33eb76c3c32f'
down_revision = '4b28ce000424'


def upgrade():
    op.add_column('photo_category', sa.Column(
        'name', sa.String(length=32), nullable=False))
    op.add_column('photo_collection', sa.Column(
        'name', sa.String(length=32), nullable=False))
    op.add_column('photo_collection', sa.Column(
        'category_id', sa.Integer(), nullable=True))
    op.create_foreign_key('photo_collection_category_id_fkey',
                          'photo_collection', 'photo_category',
                          ['category_id'], ['id'])
    op.add_column('photo_collection', sa.Column(
        'introduce', sa.String(length=256), nullable=True))
    op.add_column('photo_collection',
                  sa.Column('date', sa.Date(), nullable=True))


def downgrade():
    op.drop_column('photo_collection', 'date')
    op.drop_constraint('photo_collection_category_id_fkey', 'photo_collection',
                       type_='foreignkey')
    op.drop_column('photo_collection', 'style_id')
    op.drop_column('photo_collection', 'introduce')
    op.drop_column('photo_collection', 'category_id')
    op.drop_column('photo_collection', 'name')
    op.drop_column('photo_category', 'name')
