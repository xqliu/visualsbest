# encoding: utf-8

import os

DEBUG = True
BABEL_DEFAULT_LOCALE = 'zh_CN'
BABEL_DEFAULT_TIMEZONE = 'CST'
SQLALCHEMY_ECHO = True
# if os.environ['VISUALS_BEST_DATABASE_URL'] is not None:
try:
    SQLALCHEMY_DATABASE_URI = os.environ['VISUALS_BEST_DATABASE_URL']
except KeyError:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SECRET_KEY = '123QWEasDzXcqazw'
