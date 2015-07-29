# coding=utf-8
from flask import Flask
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
# 'python manage.py db migrate'
#   - generate migration script from current schema version.
# 'python manage.py db upgrade'
#   - migrate DB.

import app.config as config
application = Flask(__name__)
application.config.from_object(config)

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(application)
from app.app_provider import AppInfo
AppInfo.set_app(application)
AppInfo.set_db(db)

# 本行必须在 db初始化之后调用，不然会报
# AttributeError: 'NoneType' object has no attribute 'Model'
# 的错误
from app.models import *
db.init_app(application)
migrate = Migrate(application, db)
manager = Manager(application)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

@application.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()