# encoding=utf-8
from app import app_provider
from app.forms import UserRegisterForm
from app.models import Image
from app.util import file_util
from flask import render_template
from flask.ext.security import LoginForm
import os

gallery_service = app_provider.AppInfo.get_galleries_store_service()


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


def save_user_gallery(user, image):
    """
    保存用户的头像
    :param user: 用户对象
    :param image: 图像对象
    :return: None
    """
    if user.image is not None:
        existing_img = gallery_service.path(user.image.path)
        file_util.silent_remove(existing_img)
    else:
        image = Image()
        user.image = image
    filename = gallery_service.save(image)
    user.image.path = filename
    user.image.alt = u'头像'
