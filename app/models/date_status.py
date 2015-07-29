# encoding: utf-8

from app.app_provider import AppInfo
from app.models import User
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import backref, relationship

db = AppInfo.get_db()


class DateStatus(db.Model):
    """
    某摄影师某时间段的状态记录，默认只记录不可用的时间段
    """
    __tablename__ = 'date_status'
    id = Column(Integer, primary_key=True)

    # 该时间状态的所属摄影师
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relation(User, backref=backref('data_statuses',
                                             uselist=True, cascade='all, delete-orphan'))

    # 开始时间
    start_date = Column(DateTime, nullable=False)
    # 结束时间
    end_date = Column(DateTime, nullable=False)

    # 这段时间内的可用状态
    status_id = Column(Integer, ForeignKey('enum_values.id'), nullable=False)
    status = relationship('EnumValues', foreign_keys=[status_id])
