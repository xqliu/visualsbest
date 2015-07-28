# coding=utf-8

from app_provider import AppInfo
from models.image import Image
from models.photo_collection import PhotoCollection
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import backref, relationship

db = AppInfo.get_db()


class PhotoWorkImage(db.Model):
    __tablename__ = 'photo_work_image'
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey(Image.id))
    image = db.relation(Image, backref='image_photo_work')
    photo_work_id = db.Column(db.Integer, db.ForeignKey(PhotoWork.id))
    photo_work = db.relation(PhotoWork, backref='photo_work_image')    


class PhotoWork(db.Model):
    __tablename__ = 'photo_work'
    id = Column(Integer, primary_key=True)

    # 该照片作品所属的影集
    photo_collection_id = Column(Integer, ForeignKey(PhotoCollection.id), nullable=False)
    photo_collection = db.relation(PhotoCollection, backref=backref('photos', uselist=True))

    # 可选的，对作品的描述
    remark = Column(Text, nullable=True)
