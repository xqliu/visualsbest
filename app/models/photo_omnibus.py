# coding=utf-8

from app.app_provider import AppInfo
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import backref, relationship

db = AppInfo.get_db()


class PhotoOmnibus(db.Model):
    """
    主推的照片列表
    """
    __tablename__ = 'photo_omnibus'
    id = Column(Integer, primary_key=True)

    # 主推名称
    name = db.Column(db.String(32), nullable=False)

    # 标题显示的class
    title_class = db.Column(db.String(16), nullable=True)

    # 所使用的模板
    template_id = Column(Integer, ForeignKey('omnibus_template.id'), nullable=False)
    template = relationship('OmnibusTemplate', backref=backref('omnibuses', uselist=True))
