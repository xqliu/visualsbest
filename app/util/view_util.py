# encoding=utf-8
import uuid
from app import app_provider
from app.forms import UserRegisterForm
from app.models import Image
from app.util import file_util
from flask import render_template
from flask.ext.security import LoginForm
import os

gallery_service = app_provider.AppInfo.get_galleries_store_service()
image_service = app_provider.AppInfo.get_image_store_service()


def render_template_front_layout(template_html, **args):
    return render_template(template_html, login_user_form=LoginForm(),
                           register_user_form=UserRegisterForm(), **args)


def default_date_formatter(view, context, model, name):
    """
    默认的日期格式化器，格式化为 四位年/两位月/两位日
    :param view: View
    :param context: Context
    :param model: 模型
    :param name: 该字段的名称
    :return:
    """
    value = getattr(model, name)
    if value is not None:
        return value.strftime("%Y/%m/%d")
    return ''


def save_image(service, owner, image_file):
    """
    保存图片
    :param service: 用于保存图片的Flask-upload 服务
    :param owner: 该图片所属的对象，要求使用 owner.image来引用到要保存的图片
    :param image_file: 图片数据文件
    :return:
    """
    if owner.image is not None:
        existing_img = image_service.path(owner.image.path)
        file_util.silent_remove(existing_img)
    else:
        image = Image()
        owner.image = image
    name, ext = os.path.splitext(image_file.filename)
    safe_name = str(uuid.uuid4()) + ext
    filename = service.save(image_file, name=safe_name)
    owner.image.path = filename


def save_user_gallery(user, image_file):
    """
    保存用户的头像
    :param user: 用户对象
    :param image: 图像对象
    :return: None
    """
    save_image(gallery_service, user, image_file)


def save_photo_work_image(photo_work, image_file):
    """
    保存摄影师的摄影作品图片
    :param photo_work: 摄影作品对象
    :param image_file: 图片对象
    :return:
    """
    save_image(image_service, photo_work, image_file)
