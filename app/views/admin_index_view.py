# coding=utf-8
from flask import url_for, request
import flask_admin as admin
from flask.ext.security import current_user, logout_user, login_user, LoginForm, url_for_security
from werkzeug.utils import redirect
from flask_admin import helpers, expose


class AdminMainView(admin.AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated():
            return redirect(url_for('.login_view'))
        return super(AdminMainView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            if form.validate():
                login_user(form.user)

        if current_user.is_authenticated():
            return redirect(url_for('.index'))
        return redirect(url_for_security('login', next=url_for('.index')))

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))
