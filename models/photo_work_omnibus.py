# coding=utf-8

from app_provider import AppInfo
from models.image import Image
from models.photo_collection import PhotoCollection
from models.photo_omnibus import PhotoOmnibus
from models.photo_work import PhotoWork
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import backref, relationship

db = AppInfo.get_db()


class PhotoWorkOmnibus(db.Model):
    """
    主推的照片和主推之间的关联
    """
    __tablename__ = 'photo_work_image'
    id = db.Column(db.Integer, primary_key=True)

    # 主推
    photo_omnibus_id = Column(Integer, ForeignKey(PhotoOmnibus.id), nullable=False)
    photo_collection = db.relation(PhotoOmnibus, backref=backref('photos', uselist=True))

    # 照片
    photo_work_id = Column(Integer, ForeignKey(PhotoWork.id), nullable=False)
    photo_work = db.relation(PhotoWork, backref=backref('omnibuses', uselist=True))

