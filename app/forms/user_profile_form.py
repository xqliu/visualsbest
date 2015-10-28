# encoding=utf-8
from app import const
from app.models import EnumValues
from flask.ext.security.forms import Form, Required
from wtforms import StringField, RadioField, DateField, SelectField, BooleanField
from wtforms.fields.html5 import DecimalField
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
    location = SelectField('Location')
    daily_price = DecimalField('Daily Price', validators=(Required(),))
    accept_travel = BooleanField('Accept Travel')

    def __init__(self):
        super(UserProfileForm, self).__init__()
        locations = EnumValues.type_filter(const.LOCATION_TYPE_KEY).all()
        loc = []
        for s in locations:
            loc.append((str(s.id), s.display))
        self.location.choices = loc
