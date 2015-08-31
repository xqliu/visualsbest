from flask.ext.security.forms import Required
from flask_wtf import Form
from wtforms import DateField


class DateStatusForm(Form):
    from_day = DateField('from_day', validators=(Required(),))
    end_day = DateField('end_day', validators=(Required(),))
