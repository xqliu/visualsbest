# coding=utf-8

from app.app_provider import AppInfo
from app.models import Image
from app.models import PhotoCollection
from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import backref, relationship

db = AppInfo.get_db()


class PhotoWorkImage(db.Model):
    """
    与具体图片作品的关联
    """
    __tablename__ = 'photo_work_image'
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey(Image.id))
    image = db.relation(Image, backref='image_photo_work')
    photo_work_id = db.Column(db.Integer, db.ForeignKey(PhotoWork.id))
    photo_work = db.relation(PhotoWork, backref='photo_work_image')    


class PhotoWorkComment(db.Model):
    """
    作品评价，可以有文字说明
    """
    __tablename__ = 'photo_work_comment'
    id = Column(Integer, primary_key=True)

    # 关联作品
    photo_work_id = Column(Integer, ForeignKey('photo_work.id'), nullable=False)
    photo_work = relationship('PhotoWork', foreign_keys=[photo_work_id],
                              backref=backref('photo_work_comments', uselist=True))

    # 关联的评论
    comment_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    comment = relationship('Order', foreign_keys=[comment_id],
                           backref=backref('associated_photo_work', uselist=False))


class PhotoWorkFavourite(db.Model):
    """
    作品收藏
    """
    __tablename__ = 'photo_work_favourite'
    id = Column(Integer, primary_key=True)

    # 关联作品
    photo_work_id = Column(Integer, ForeignKey('photo_work.id'), nullable=False)
    photo_work = relationship('PhotoWork', foreign_keys=[photo_work_id],
                              backref=backref('associated_favourites', uselist=True))

    # 关联的评论
    favourite_id = Column(Integer, ForeignKey('favourite.id'), nullable=False)
    favourite = relationship('Favourite', foreign_keys=[favourite_id],
                             backref=backref('associated_photo_work', uselist=False))


class PhotoWork(db.Model):
    """
    摄影作品
    """
    __tablename__ = 'photo_work'
    id = Column(Integer, primary_key=True)

    # 该照片作品所属的影集
    photo_collection_id = Column(Integer, ForeignKey(PhotoCollection.id), nullable=False)
    photo_collection = db.relation(PhotoCollection, backref=backref('photos', uselist=True))

    # 可选的，对作品的描述
    remark = Column(Text, nullable=True)
