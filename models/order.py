# coding=utf-8

from app_provider import AppInfo
from models.request import Request
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import backref, relationship

db = AppInfo.get_db()


class Order(db.Model):
    """
    订单，在用户的拍摄请求被摄影师确认后，订单会被自动创建
    """
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)

    # 与订单关联的请求
    request_id = db.Column(db.Integer, db.ForeignKey(Request.id))
    request = db.relation(Request, backref=backref(
        'associated_order', uselist=False))

    # 订单的状态，可以由平台或者摄影师标记为以付款
    status_id = Column(Integer, ForeignKey('enum_values.id'), nullable=False)
    status = relationship('EnumValues', foreign_keys=[status_id])

