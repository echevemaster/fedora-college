from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import Required
from fedora_college.core.models import Screencast


class AddScreenCast(Form):
    name = TextField('Name', [Required()])
    desc = TextAreaField('Description')
