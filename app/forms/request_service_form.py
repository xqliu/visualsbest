from flask.ext.security.forms import Required
from flask_wtf import Form
from wtforms import StringField, SelectField
from wtforms.fields.html5 import DecimalField, DateField
from wtforms.validators import Optional


class RequestServiceForm(Form):
    photographer_id = StringField('photographer_id', [Required()])
    requester_id = StringField('requester_id', [Required()])
    from_day = DateField('from_day', validators=(Required(),))
    end_day = DateField('end_day', validators=(Required(),))
    category = SelectField('category', [Required()])
    style = SelectField('style', [Required()])
    lens_needed = StringField('lens_needed', [Required()])
    remark = StringField('remark', [Optional()])
    location = StringField('location', [Required()])
    price = DecimalField('price', [Optional()])
    amount = DecimalField('amount', [Optional()])

    def __init__(self, categories, styles):
        super(RequestServiceForm, self).__init__()
        cats = []
        for c in categories:
            cats.append((str(c.id), c.display))
        self.category.choices = cats
        scs = []
        for s in styles:
            scs.append((str(s.id), s.display))
        self.style.choices = scs

