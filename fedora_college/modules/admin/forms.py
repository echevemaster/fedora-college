# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, FileField, \
    BooleanField
from wtforms.validators import Required

__all__ = ['AddScreenCast']


class AddScreenCast(Form):
    title = TextField('Title', [Required()])
    slug = TextField('Slug', [Required()])
    description = TextAreaField('Content', [Required()])
    url_video = FileField('Upload a video', [Required()])
    active = BooleanField('Enabled?', [Required()])
