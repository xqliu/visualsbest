# coding=utf-8

from app.app_provider import AppInfo
from user import User
from sqlalchemy import Column, Integer, ForeignKey, String, Date, Numeric
from sqlalchemy.orm import backref, relationship

db = AppInfo.get_db()


class PhotoCollection(db.Model):
    """
    照片列表
    """
    __tablename__ = 'photo_collection'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    introduce = Column(String(256), nullable=False)
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

    # 作品所属的风格
    style_id = Column(Integer, ForeignKey('enum_values.id'), nullable=False)
    style = relationship('EnumValues', backref=backref(
        'photo_collections_of_style', uselist=True), foreign_keys=[style_id])

    # 作品所属的分类
    category_id = Column(Integer, ForeignKey('enum_values.id'), nullable=True)
    category = relationship('EnumValues', backref=backref(
        'photo_collections_of_category', uselist=True),
                            foreign_keys=[category_id])

    # 作品的拍摄时间
    date = db.Column(Date, nullable=True)

    # 价格
    price = Column(Numeric(precision=8, scale=2, decimal_return_scale=2),
                   nullable=True)


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
