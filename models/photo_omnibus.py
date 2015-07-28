# coding=utf-8

from app_provider import AppInfo
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import backref, relationship

db = AppInfo.get_db()


class PhotoOmnibus(db.Model):
    """
    主推的照片列表
    """
    __tablename__ = 'photo_omnibus'
    id = Column(Integer, primary_key=True)    