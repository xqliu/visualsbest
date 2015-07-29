# coding=utf-8

from app_provider import AppInfo
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import backref, relationship

db = AppInfo.get_db()


class OmnibusTemplate(db.Model):
    """
    主推的照片列表的模板
    """
    __tablename__ = 'omnibus_template'
    id = Column(Integer, primary_key=True)