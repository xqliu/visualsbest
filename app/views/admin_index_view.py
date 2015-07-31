# coding=utf-8
import app.app_provider
from flask import url_for, request
from flask.ext.admin.consts import ICON_TYPE_GLYPH
from flask.ext.babelex import lazy_gettext
import flask_admin as admin
from flask.ext.security import current_user, logout_user, login_user, login_required
from login_form import LoginForm
from werkzeug.utils import redirect
from flask_admin import helpers, expose


class AdminMainView(admin.AdminIndexView):
    @expose('/')
    def index(self):
        return redirect(url_for('user.index_view'))