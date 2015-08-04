# coding=utf-8

from app.app_provider import AppInfo
from user import User
from sqlalchemy import Column, Integer
from sqlalchemy.orm import backref

db = AppInfo.get_db()


class PhotoCategory(db.Model):
    """
    照片分类(风景、运动、人像等)，由摄影师创建
    """
    __tablename__ = 'photo_category'
    id = Column(Integer, primary_key=True)

    # 该分类所属于的用户
    photographer_id = db.Column(db.Integer, db.ForeignKey(User.id))
    photographer = db.relation(User, backref=backref(
        'photo_categories', uselist=True, cascade='all, delete-orphan'))
