# encoding=utf-8
from flask.ext.security.forms import Required
from flask_wtf import Form
from wtforms import StringField, SelectField
from wtforms.fields.html5 import DecimalField


class PhotoCollectionForm(Form):
    name = StringField('name', [Required()])
    introduce = StringField('introduce', [Required()])
    category = SelectField('category', [Required()])
    style = SelectField('style', [Required()])
    price = DecimalField('price', [Required()])

    def __init__(self, categories, styles):
        super(PhotoCollectionForm, self).__init__()
        cats = []
        for c in categories:
            cats.append((str(c.id), c.display))
        self.category.choices = cats
        scs = []
        for s in styles:
            scs.append((str(s.id), s.display))
        self.style.choices = scs
