# encoding=utf-8
from flask.ext.security.forms import Form, Required
from wtforms import StringField, RadioField, DateField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import Optional


class UserProfileForm(Form):
    login = StringField('Login', [Required()])
    display = StringField('Display', [Required()])
    mobile_phone = StringField('Mobile Phone', [Required()])
    email = StringField('Email Address', [Required()])
    gender = RadioField('gender', choices=[(u'男', u'男'),
                                           (u'女', u'女'),
                                           (u'保密', u'保密')])
    birthday = DateField('birthday', validators=(Optional(),))
    qq_number = StringField('QQ Number')
    weibo_account = StringField('Weibo Account')
    wechat_account = StringField('Wechat Account')
    introduce = StringField('Introduce')
