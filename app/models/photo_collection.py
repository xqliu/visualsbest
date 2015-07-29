# coding=utf-8

from app.app_provider import AppInfo
from app.models import User
from sqlalchemy import Column, Integer
from sqlalchemy.orm import backref

db = AppInfo.get_db()


class PhotoCollection(db.Model):
    """
    照片列表
    """
    __tablename__ = 'photo_collection'
    id = Column(Integer, primary_key=True)
    # 作品的作者摄影师
    photographer_id = db.Column(db.Integer, db.ForeignKey(User.id))
    photographer = db.relation(User, backref=backref(
        'produced_photo_collections', uselist=True, cascade='all, delete-orphan'))
    # 上传作品到系统中的用户
    uploader_id = db.Column(db.Integer, db.ForeignKey(User.id))
    uploader = db.relation(User, backref=backref(
        'uploaded_photo_collections', uselist=True, cascade='all, delete-orphan'))