# coding=utf-8

from app_provider import AppInfo
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import backref, relationship

db = AppInfo.get_db()


class PhotoWorkComment(db.Model):
    __tablename__ = 'photo_work_comment'
    id = Column(Integer, primary_key=True)