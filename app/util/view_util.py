# encoding=utf-8
from app.forms import UserRegisterForm
from flask import render_template
from flask.ext.login import current_user
from flask.ext.security import LoginForm


def render_template_front_layout(template_html, **args):
    return render_template(template_html, login_user_form=LoginForm(),
                           register_user_form=UserRegisterForm(), **args)


def default_date_formatter(view, context, model, name):
    value = getattr(model, name)
    if value is not None:
        return value.strftime("%Y/%m/%d")
    return ''
