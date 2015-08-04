# coding=utf-8

from app.app_provider import AppInfo
from user import User
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import backref, relationship

db = AppInfo.get_db()


class PhotoCollection(db.Model):
    """
    照片列表
    """
    __tablename__ = 'photo_collection'
    id = Column(Integer, primary_key=True)
    # 作品的作者摄影师
    photographer_id = db.Column(db.Integer, db.ForeignKey(User.id))
    photographer = db.relation(User,
                               backref=backref('produced_photo_collections',
                                               uselist=True,
                                               cascade='all, delete-orphan'),
                               foreign_keys=[photographer_id])
    # 上传作品到系统中的用户
    uploader_id = db.Column(db.Integer, db.ForeignKey(User.id))
    uploader = db.relation(User,
                           backref=backref('uploaded_photo_collections',
                                           uselist=True,
                                           cascade='all, delete-orphan'),
                           foreign_keys=[uploader_id])


class PhotoCollectionFavourite(db.Model):
    """
    作品集收藏
    """
    __tablename__ = 'photo_collection_favourite'
    id = Column(Integer, primary_key=True)

    # 关联作品集
    photo_collection_id = Column(Integer, ForeignKey(
        'photo_collection.id'), nullable=False)
    photo_collection = relationship('PhotoCollection',
                                    foreign_keys=[photo_collection_id],
                                    backref=backref(
                                        'associated_favourites',
                                        uselist=True))

    # 关联的收藏
    favourite_id = Column(Integer, ForeignKey('favourite.id'), nullable=False)
    favourite = relationship('Favourite',
                             foreign_keys=[favourite_id],
                             backref=backref(
                                 'associated_photo_collection',
                                 uselist=False))
