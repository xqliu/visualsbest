# coding=utf-8
from flask import Flask
from flask.ext.images import Images
from flask.ext.mail import Mail
from flask.ext.migrate import Migrate
from flask.ext.security import SQLAlchemyUserDatastore, Security
import os
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception


app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

import app.config as config

app.config.from_object(config)

from flask_babelex import Babel
babel = Babel(default_locale='zh_Hans_CN')
babel.init_app(app)

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
from app.app_provider import AppInfo
AppInfo.set_app(app)
AppInfo.set_db(db)

# 初始化Gallery存储的服务，用于存储所有的用户上传的头像
from flask.ext.uploads import UploadSet, configure_uploads
from flask.ext.uploads import IMAGES
galleries_upload_set = UploadSet('gallery', IMAGES)
configure_uploads(app, galleries_upload_set)
AppInfo.set_galleries_store_service(galleries_upload_set)

# 初始化Image存储的服务，用于存储所有摄影师上传的作品图像
images_upload_set = UploadSet('images', IMAGES)
configure_uploads(app, images_upload_set)
AppInfo.set_image_store_service(images_upload_set)


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
security = Security(app, user_datastore, confirm_register_form=UserRegisterForm)

from app.views import init_admin_views
admin = init_admin_views(app, db)
AppInfo.set_admin(admin)

# 初始化 Flask-Mail 用于发送邮件
mail = Mail(app)

# 初始化Flask-Image
images = Images(app)


@app.before_first_request
def upgrade_db_schema():
    try:
        base_path = os.path.join(os.path.dirname(__file__), 'migrations')
        migrate = Migrate(app, db, directory=base_path)
        from flask.ext.migrate import upgrade
        # migrate database to latest revision
        upgrade()
    except:
        print "Error upgrade db:\n", sys.exc_info()[0], '\n', sys.exc_info()[1], '\n', sys.exc_info()[2]


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