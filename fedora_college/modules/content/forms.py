# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField
from wtforms import BooleanField, SelectField, validators
from wtforms.validators import Required

__all__ = ['CreateContent']

# form class for creating  content


class CreateContent(Form):
    title = TextField(
        'Title',  [validators.Length(min=4, max=255)])
    description = TextAreaField('Content', [validators.Length(min=4)])
    type_content = SelectField(u'Content Type',
                               [Required()],
                               choices=[('blog', 'Blog Post'),
                                        ('lecture', 'Lecture'),
                                        ('doc', 'Documentation')]
                               )

    category = TextField(u'category', [Required()])
    # Comma seprated media id's
    active = BooleanField('Published')
    tags = TextField('Tags', [Required()])
    # Comma seprated tag id's
