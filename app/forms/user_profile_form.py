# encoding=utf-8
from app import const
from app.models import EnumValues
from flask.ext.security.forms import Form, Required
from wtforms import StringField, RadioField, DateField, SelectMultipleField
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
    users_styles = SelectMultipleField('users_styles')
    daily_price = DecimalField('daily_price', validators=(Required(),))

    def __init__(self):
        super(UserProfileForm, self).__init__()
        styles = EnumValues.type_filter(const.PHOTO_STYLE_KEY).all()
        scs = []
        for s in styles:
            scs.append((str(s.id), s.display))
        self.users_styles.choices = scs
