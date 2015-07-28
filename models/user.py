# coding=utf-8

from app_provider import AppInfo
from models.image import Image
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import backref, relationship

db = AppInfo.get_db()


class User(db.Model):
    __tablename__ = 'user'    
    id = Column(Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey(Image.id))
    image = db.relation(Image, backref='image_user')

    # 用户类型
    type_id = Column(Integer, ForeignKey('enum_values.id'), nullable=False)
    type = relationship('EnumValues', backref=backref(
        'users_of_this_type', uselist=True))