# coding=utf-8

from app.app_provider import AppInfo
import os.path as op
from sqlalchemy import event
import os

db = AppInfo.get_db()

# Figure out base upload path
base_path = op.join(op.dirname(__file__), 'static')


class Image(db.Model):
    """
    作品关联的图片文件的元数据
    """
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    alt = db.Column(db.Unicode(256))
    path = db.Column(db.String(128), nullable=False)


# Register after_delete handler which will delete image file after model gets deleted
@event.listens_for(Image, 'after_delete')
def _handle_image_delete(mapper, conn, target):
    """
    在删除了图片实体时，同时删除相关联的图片文件
    :param mapper:
    :param conn:
    :param target:
    :return:
    """
    try:
        if target.path:
            os.remove(op.join(base_path, target.path))
    except:
        pass    