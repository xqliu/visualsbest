# coding=utf-8
import sys
from flask import Flask, url_for, redirect, render_template
from flask.ext.migrate import Migrate, Config, MigrateCommand
from flask.ext.script import Manager
from flask.ext.security import SQLAlchemyUserDatastore, Security, login_required, LoginForm
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

# 本行必须在 db初始化之后调用，不然会报
# AttributeError: 'NoneType' object has no attribute 'Model'
# 的错误
from app.models import *

db.init_app(app)

# Setup Flask-Security
from app.models.user import User, Role, roles_users

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from app.views import init_admin_views

admin = init_admin_views(app, db)
AppInfo.set_admin(admin)


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
    return render_template('index.html', login_user_form=LoginForm())


@app.route("/works")
def works():
    return render_template('works.html', login_user_form=LoginForm())


@app.route("/work_details")
def work_details():
    return render_template('work_details.html', login_user_form=LoginForm())


@app.route("/photograph")
def photograph():
    return render_template('photograph.html', login_user_form=LoginForm())


@app.route("/search")
def search():
    return render_template('search.html', login_user_form=LoginForm())


@app.route("/comments")
def comments():
    return render_template('comments.html', login_user_form=LoginForm())


@app.route("/create_collection")
@login_required
def create_collection():
    return render_template('create_collection.html', login_user_form=LoginForm())


@app.route("/blog")
def blog():
    return render_template('blog.html', login_user_form=LoginForm())


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', login_user_form=LoginForm())


@app.route("/my_photos")
@login_required
def my_photos():
    return render_template('my_photos.html', login_user_form=LoginForm())


@app.route("/orders")
@login_required
def orders():
    return render_template('orders.html', login_user_form=LoginForm())


@app.route("/messages")
@login_required
def messages():
    return render_template('messages.html', login_user_form=LoginForm())


@app.route("/settings")
@login_required
def settings():
    return render_template('settings.html', login_user_form=LoginForm())

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=80, debug=True)
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.run()
