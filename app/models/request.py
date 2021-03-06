# coding=utf-8

from app.app_provider import AppInfo
from app.const import PHOTO_CATEGORY_KEY, PHOTO_STYLE_KEY, REQUEST_STATUS_KEY, REQUEST_STATUS_CANCELLED, REQUEST_STATUS_DRAFT
from app.models import EnumValues
from user import User
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import backref, relationship

db = AppInfo.get_db()


class Request(db.Model):
    """
    用户发起的拍摄请求
    """
    __tablename__ = 'request'
    id = Column(Integer, primary_key=True)

    # 提起申请的用户
    requester_id = db.Column(db.Integer, db.ForeignKey(User.id))
    requester = db.relation(User, backref=backref('sent_requests', uselist=True, cascade='all, delete-orphan'),
                            foreign_keys=[requester_id])

    # 接收申请的用户
    photographer_id = db.Column(db.Integer, db.ForeignKey(User.id))
    photographer = db.relation(User, backref=backref('received_requests', uselist=True), foreign_keys=[photographer_id])

    # 开始时间
    start_date = Column(DateTime, nullable=False)
    # 结束时间
    end_date = Column(DateTime, nullable=False)

    # 作品所属的风格
    style_id = Column(Integer, ForeignKey('enum_values.id'), nullable=True)
    style = relationship('EnumValues', backref=backref('request_of_style', uselist=True),
                         foreign_keys=[style_id])

    # 作品所属的分类
    category_id = Column(Integer, ForeignKey('enum_values.id'), nullable=True)
    category = relationship('EnumValues', backref=backref('request_of_category', uselist=True),
                            foreign_keys=[category_id])
    # 拍摄地点
    location_id = Column(Integer, ForeignKey('enum_values.id'), nullable=True)
    location = relationship('EnumValues', backref=backref('requests_of_location', uselist=True), foreign_keys=[location_id])

    # 需要带的镜头
    lens_needed = Column(String(128))
    # 其他备注信息
    remark = Column(String(512))
    # 单价
    price = Column(Numeric(precision=8, scale=2, decimal_return_scale=2), nullable=True)
    # 总价
    amount = Column(Numeric(precision=8, scale=2, decimal_return_scale=2), nullable=True)

    # 请求的状态，可能为拒绝或者同意，同意的会自动转变为订单
    status_id = Column(Integer, ForeignKey('enum_values.id'), nullable=False)
    status = relationship('EnumValues', foreign_keys=[status_id])

    @staticmethod
    def category_filter():
        return EnumValues.type_filter(PHOTO_CATEGORY_KEY)

    @staticmethod
    def style_filter():
        return EnumValues.type_filter(PHOTO_STYLE_KEY)

    @staticmethod
    def status_filter():
        return EnumValues.type_filter(REQUEST_STATUS_KEY)

    @staticmethod
    def draft_status_filter():
        return db.session.query(Request).join(EnumValues, Request.status_id == EnumValues.id).filter_by(code=REQUEST_STATUS_DRAFT)

    def __repr__(self):
        return self.requester.display + '->' + self.photographer.display + ' @ [' \
               + self.start_date.strftime('%Y/%m/%d') + ' TO ' + self.end_date.strftime('%Y/%m/%d') + '] @ ' \
               + str(self.location or '未知地点')
