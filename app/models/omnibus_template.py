# coding=utf-8

from app.app_provider import AppInfo
from sqlalchemy import Column, Integer

db = AppInfo.get_db()


class OmnibusTemplate(db.Model):
    """
    主推的照片列表的模板
    """
    __tablename__ = 'omnibus_template'
    id = Column(Integer, primary_key=True)

    # 模板名称
    name = db.Column(db.String(32), nullable=False)

    # 主推的显示模板的路径
    path = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return self.name
