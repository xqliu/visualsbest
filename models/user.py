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
        'users_of_type', uselist=True))

    # 用户状态
    status_id = Column(Integer, ForeignKey('enum_values.id'), nullable=False)
    status = relationship('EnumValues', backref=backref(
        'users_of_status', uselist=True))

    # 该用户是由哪个用户推荐的
    recommend_by_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    recommend_by = db.relation("User", remote_side=id, backref=backref(
        'recommended_users', uselist=True))