# coding=utf-8
from flask import Flask, url_for, redirect
from flask.ext.security import SQLAlchemyUserDatastore, Security
import os
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

app = Flask(__name__)

import config as config

app.config.from_object(config)

from flask_babelex import Babel
babel = Babel(default_locale='zh_Hans_CN')
babel.init_app(app)

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
from app_provider import AppInfo
AppInfo.set_app(app)
AppInfo.set_db(db)

# 本行必须在 db初始化之后调用，不然会报
# AttributeError: 'NoneType' object has no attribute 'Model'
# 的错误
from models import *
db.init_app(app)

# Setup Flask-Security
from models.user import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from views import init_admin_views
admin = init_admin_views(app, db)
AppInfo.set_admin(admin)


@app.before_first_request
def init_rollbar():
    """init rollbar module"""
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


@app.route("/")
def index():
    return redirect(url_for('static', filename='index.html'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
