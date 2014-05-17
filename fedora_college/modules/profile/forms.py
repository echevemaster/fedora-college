# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import Required

#__all__ = ['EditProfile']


class EditProfile(Form):

    username = TextField('Username', [Required()])
    email = TextField('Email', [Required()])
    about = TextAreaField('About', [Required()])
    website = TextField('Website', [Required()])
