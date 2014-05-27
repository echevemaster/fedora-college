# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, BooleanField, SelectField, validators
from wtforms.validators import Required

__all__ = ['CreateContent']


class CreateContent(Form):
    title = TextField(
        'Title',  [validators.Length(min=4, max=255)])
    slug = TextField(
        'Url-Slug', [validators.Length(min=4, max=255)])
    description = TextAreaField('Content', [validators.Length(min=4)])
    media_added_ids = TextField('media')
    type_content = SelectField(u'Cntent Type',
                               [Required()],
                               choices=[('blog', 'Blog Post'),
                                        ('media', 'Lecture'),
                                        ('doc', 'Documentation')]
                               )
    # Comma seprated media id's
    active = BooleanField('Published')
    tags = TextField('Tags', [Required()])
    # Comma seprated tag id's
