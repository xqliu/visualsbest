# coding=utf-8

from app.app_provider import AppInfo
from app.models import User
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import backref

db = AppInfo.get_db()


class UserExperience(db.Model):
    """
    用户的经历
    """
    __tablename__ = 'user_experience'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)

    # 该经历所属的用户
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relation(User, backref=backref(
        'experience', uselist=False, cascade='all, delete-orphan'))