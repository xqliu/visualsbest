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
    type_id = StringField('User Type', [Required()])
    status_id = StringField('Verify Status', [Required()])
    normal_user_type = EnumValues.find_one_by_code('NORMAL_USER')
    photographer_user_type = EnumValues.find_one_by_code('PHOTOGRAPHER_USER')
    status = EnumValues.find_one_by_code('UN_VERIFIED')


