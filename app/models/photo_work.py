# coding=utf-8

from app.app_provider import AppInfo
from image import Image
from photo_omnibus import PhotoOmnibus
from photo_collection import PhotoCollection
from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import backref, relationship

db = AppInfo.get_db()


class PhotoWork(db.Model):
    """
    摄影作品
    """
    __tablename__ = 'photo_work'
    id = Column(Integer, primary_key=True)

    # 该照片作品所属的影集
    photo_collection_id = Column(Integer, ForeignKey(PhotoCollection.id),
                                 nullable=False)
    photo_collection = db.relation(PhotoCollection,
                                   backref=backref('photos', uselist=True))

    # 该作品的图片对象
    image_id = db.Column(db.Integer, db.ForeignKey(Image.id))
    image = db.relation(Image, backref='image_photo_work')

    # 可选的，对作品的描述
    remark = Column(Text, nullable=True)


class PhotoWorkComment(db.Model):
    """
    作品评价，可以有文字说明
    """
    __tablename__ = 'photo_work_comment'
    id = Column(Integer, primary_key=True)

    # 关联作品
    photo_work_id = Column(Integer, ForeignKey('photo_work.id'),
                           nullable=False)
    photo_work = relationship('PhotoWork', foreign_keys=[photo_work_id],
                              backref=backref('photo_work_comments',
                                              uselist=True))

    # 关联的评论
    comment_id = Column(Integer, ForeignKey('comment.id'), nullable=False)
    comment = relationship('Comment', foreign_keys=[comment_id],
                           backref=backref('associated_photo_work',
                                           uselist=False))


class PhotoWorkFavourite(db.Model):
    """
    作品收藏
    """
    __tablename__ = 'photo_work_favourite'
    id = Column(Integer, primary_key=True)

    # 关联作品
    photo_work_id = Column(Integer, ForeignKey(
        'photo_work.id'), nullable=False)
    photo_work = relationship('PhotoWork', foreign_keys=[photo_work_id],
                              backref=backref('associated_favourites',
                                              uselist=True))

    # 关联的收藏
    favourite_id = Column(Integer, ForeignKey('favourite.id'), nullable=False)
    favourite = relationship('Favourite', foreign_keys=[favourite_id],
                             backref=backref('associated_photo_work',
                                             uselist=False))


class PhotoWorkOmnibus(db.Model):
    """
    主推的照片和主推之间的关联
    """
    __tablename__ = 'photo_work_omnibus'
    id = db.Column(db.Integer, primary_key=True)

    # 主推
    photo_omnibus_id = Column(Integer, ForeignKey(
        PhotoOmnibus.id), nullable=False)
    photo_omnibus = db.relation(
        PhotoOmnibus, backref=backref('photo_works', uselist=True))

    # 照片
    photo_work_id = Column(Integer, ForeignKey(PhotoWork.id), nullable=False)
    photo_work = db.relation(
        PhotoWork, backref=backref('omnibuses', uselist=True))

    # 该作品放置的行
    work_row = Column(Integer, nullable=False)

    # 该作品放置的列
    work_col = Column(Integer, nullable=False)
