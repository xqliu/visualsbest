# coding=utf-8

from app_provider import AppInfo
from models.image import Image
from models.user import User
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import backref, relationship

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