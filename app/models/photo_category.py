# coding=utf-8

from app.app_provider import AppInfo
from user import User
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import backref

db = AppInfo.get_db()


class PhotoCategory(db.Model):
    """作品分类，由摄影师创建"""
    __tablename__ = 'photo_category'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)

    # 该分类所属于的用户
    photographer_id = db.Column(db.Integer, db.ForeignKey(User.id))
    photographer = db.relation(User, backref=backref(
        'photo_categories', uselist=True, cascade='all, delete-orphan'))
