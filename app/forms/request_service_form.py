from flask.ext.security.forms import Required
from flask_wtf import Form
from wtforms import StringField, SelectField
from wtforms.fields.html5 import DecimalField, DateField
from wtforms.validators import Optional


def list_from_enum_values(enum_values):
    values = []
    for v in enum_values:
        values.append((str(v.id), v.display))
    return values


class RequestServiceForm(Form):
    photographer_id = StringField('photographer_id', [Required()])
    requester_id = StringField('requester_id', [Required()])
    start_date = DateField('from_day', validators=(Required(),))
    end_date = DateField('end_day', validators=(Required(),))
    category = SelectField('category', [Required()])
    style = SelectField('style', [Required()])
    lens_needed = StringField('lens_needed', [Required()])
    remark = StringField('remark', [Optional()])
    location = SelectField('Location', [Required()])
    price = DecimalField('price', [Required()])
    amount = DecimalField('amount', [Optional()])

    def __init__(self, categories, styles, locations):
        super(RequestServiceForm, self).__init__()
        self.category.choices = list_from_enum_values(categories)
        self.location.choices = list_from_enum_values(locations)
        self.style.choices = list_from_enum_values(styles)
