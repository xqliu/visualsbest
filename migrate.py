# coding=utf-8
from flask import Flask
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.security import SQLAlchemyUserDatastore, Security

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

import app.config as config

app.config.from_object(config)

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
from app.app_provider import AppInfo

AppInfo.set_app(app)
AppInfo.set_db(db)

# Setup Flask-Security
from app.models.user import User, Role
# Set up flask security messages.
for key, value in config.security_messages.items():
    app.config['SECURITY_MSG_' + key] = value
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
from app.forms.register_form import UserRegisterForm
security = Security(app, user_datastore, confirm_register_form=UserRegisterForm)


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=80, debug=True)
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.run()
