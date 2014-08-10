# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, validators
from wtforms.validators import Required

__all__ = ['AddComment']

# Add comment form


class AddComment(Form):
    text = TextField(
        'Text',  [validators.Length(min=4, max=2048)])
    content_id = TextField('Content ID', [Required()])
