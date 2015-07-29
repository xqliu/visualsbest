# coding=utf-8

from app.app_provider import AppInfo
from request import Request
from sqlalchemy import Column, Integer, ForeignKey
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
    status = relationship('EnumValues', foreign_keys=[status_id],
                          backref=backref('orders_with_status', uselist=True))


class OrderComment(db.Model):
    """
    订单评价，可以有文字说明和评分
    """
    __tablename__ = 'order_comment'
    id = Column(Integer, primary_key=True)

    # 关联订单
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    order = relationship('Order', foreign_keys=[order_id],
                         backref=backref('order_comments', uselist=True))

    # 关联的评论
    comment_id = Column(Integer, ForeignKey('comment.id'), nullable=False)
    comment = relationship('Comment', foreign_keys=[comment_id],
                           backref=backref('order_comment', uselist=False))

    # 评分星级，1到5, 对于用户发起的订单评论，可能有 Rating
    rating = Column(Integer, nullable=True)



