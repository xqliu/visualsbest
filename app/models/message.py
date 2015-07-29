# coding=utf-8

from app.app_provider import AppInfo
from app.models import User
from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import backref, relationship

db = AppInfo.get_db()


class Message(db.Model):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    # 发送消息的人
    from_user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    from_user = db.relation(User, backref=backref('sent_messages',
                                                  uselist=True, cascade='all, delete-orphan'))
    # 接收消息的人
    receive_user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    receive_user = db.relation(User, backref=backref('received_messages',
                                                     uselist=True, cascade='all, delete-orphan'))

    # 消息内容
    content = Column(Text, nullable=False)

    # 消息发送时间
    date = Column(DateTime, nullable=False)

    # 消息状态
    status_id = Column(Integer, ForeignKey('enum_values.id'), nullable=False)
    status = relationship('EnumValues', foreign_keys=[status_id])

