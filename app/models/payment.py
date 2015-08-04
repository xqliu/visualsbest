# coding=utf-8

from app.app_provider import AppInfo
from sqlalchemy import Column, Integer

db = AppInfo.get_db()


class Payment(db.Model):
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True)
