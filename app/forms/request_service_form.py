from flask.ext.security.forms import Required
from flask_wtf import Form
from wtforms import StringField, SelectField
from wtforms.fields.html5 import DecimalField, DateField


class RequestServiceForm(Form):
    from_day = DateField('from_day', validators=(Required(),))
    end_day = DateField('end_day', validators=(Required(),))
    style = SelectField('style', [Required()])
    price = DecimalField('price')
    location = StringField('location', [Required()])
    lens_needed = StringField('lens_needed', [Required()])

    def __init__(self, styles):
        super(RequestServiceForm, self).__init__()
        scs = []
        for s in styles:
            scs.append((str(s.id), s.display))
        self.style.choices = scs
