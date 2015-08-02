# encoding=utf-8
from app.models import EnumValues
from flask.ext.security import RegisterForm
from flask.ext.security.forms import Required
from wtforms import TextField, StringField


class UserRegisterForm(RegisterForm):
    mobile_phone = StringField('Mobile Phone', [Required()])
    login = StringField('Login', [Required()])
    display = StringField('Display', [Required()])
    email = StringField('Email', [Required()])
    # normal_user_type_id = EnumValues.find_one_by_code('')


