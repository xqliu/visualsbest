# coding=utf-8

from app.app_provider import AppInfo
from app.models import PhotoWork
from app.models import User
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import backref

db = AppInfo.get_db()


class Favourite(db.Model):
    """
    收藏，用户可以收藏某一个作品
    """
    __tablename__ = 'favourite'
    id = Column(Integer, primary_key=True)

    # 该收藏所属的用户
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relation(User, backref=backref(
        'favourites', uselist=True, cascade='all, delete-orphan'))

    # 收藏的作品
    photo_work_id = Column(Integer, ForeignKey(PhotoWork.id), nullable=True)
    photo_work = db.relation(PhotoWork, backref=backref(
        'related_favourites', uselist=True))

    # 收藏的套系
    photo_collection_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=True)
    photo_collection = db.relation(User, backref=backref(
        'related_favourites', uselist=True))
