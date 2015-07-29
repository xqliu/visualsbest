# coding=utf-8

from app.app_provider import AppInfo
from app.models import PhotoOmnibus
from app.models import PhotoWork
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import backref

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

    # 该作品放置的行
    work_row = Column(Integer, nullable=False)

    # 该作品放置的列
    work_col = Column(Integer, nullable=False)

