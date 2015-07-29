# coding=utf-8

from app_provider import AppInfo
from models.user import User
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import backref, relationship

db = AppInfo.get_db()


class Comment(db.Model):
    """
    评论，该评论可能是针对一个订单，或者一个作品
    如果针对一个订单，通过对象OrderComment进行关联
    如果针对一幅作品，通过对象PhotoWorkComment进行关联
    """
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)

    # 评论内容
    content = Column(Text, nullable=False)

    # 评论创建时间
    date = Column(DateTime, nullable=False)

    # 评论所属的用户
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relation(User, backref=backref('comments_created', uselist=True))