# coding=utf-8
from app.util.filter import jinja2_filter_substring, jinja2_filter_startswith, jinja2_filter_date_with_delta, \
    jinja2_filter_photo_collection_heat_map
from app.util.image_store import ImageStore
from flask import Flask
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.images import Images
from flask.ext.mail import Mail
from flask.ext.security import SQLAlchemyUserDatastore, Security
import os
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception
from raven.contrib.flask import Sentry

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

import app.config as config

app.config.from_object(config)

app.jinja_env.filters['substring'] = jinja2_filter_substring
app.jinja_env.filters['startswith'] = jinja2_filter_startswith
app.jinja_env.filters['datedelta'] = jinja2_filter_date_with_delta
app.jinja_env.filters['heatmap'] = jinja2_filter_photo_collection_heat_map

from flask_babelex import Babel

babel = Babel(default_locale='zh_Hans_CN')
babel.init_app(app)

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
from app.app_provider import AppInfo

AppInfo.set_app(app)
AppInfo.set_db(db)

# 初始化云端的图片存储服务
image_store = ImageStore(app)
# 初始化Gallery存储的服务，用于存储所有的用户上传的头像
AppInfo.set_galleries_store_service(image_store)
# 初始化Image存储的服务，用于存储所有摄影师上传的作品图像
AppInfo.set_image_store_service(image_store)

# 初始化调试工具栏(Flask-DebugToolbar)
toolbar = DebugToolbarExtension(app)


# 初始化所有的routers定义
from app.routers import *

# 本行需要在 app定义后， 调用了AppInfo.set_app(app)后才能包含
# 本行必须在 db初始化之后调用，不然会报
# AttributeError: 'NoneType' object has no attribute 'Model'
# 的错误
from app.models import *


# Setup Flask-Security
from app.models.user import User, Role
# Set up flask security messages.
for key, value in config.security_messages.items():
    app.config['SECURITY_MSG_' + key] = value
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
from app.forms.register_form import UserRegisterForm
from app.forms.username_login_form import UsernameLoginForm

security = Security(app, user_datastore, confirm_register_form=UserRegisterForm, login_form=UsernameLoginForm)

from app.views import init_admin_views

admin = init_admin_views(app, db)
AppInfo.set_admin(admin)

# 初始化 Flask-Mail 用于发送邮件
mail = Mail(app)

# 初始化Flask-Image
images = Images(app)

# Set Log level for werkzeug to ERROR to dismiss access log
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if config.DEBUG is not True:
    sentry = Sentry(app)


@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    if config.DEBUG is not True:
        rollbar.init(
            # access token for the demo app: https://rollbar.com/demo
            '90a56a42d47d4343a45b1105338d47c8',
            # environment name
            'heroku_development',
            # server root directory, makes tracebacks prettier
            root=os.path.dirname(os.path.realpath(__file__)),
            # flask already sets up logging
            allow_logging_basic_config=False)

        # send exceptions from `app` to rollbar, using flask's signal system.
        got_request_exception.connect(rollbar.contrib.flask.report_exception, app)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
