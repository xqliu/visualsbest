# coding=utf-8

from app_provider import AppInfo
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import backref, relationship

db = AppInfo.get_db()


class Payment(db.Model):
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True)