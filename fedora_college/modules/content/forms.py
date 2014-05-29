# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required

__all__ = ['CreateContent']


class CreateContent(Form):

    title = TextField('Title', [Required()])
    slug = TextField('Url-Slug', [Required()])
    description = TextAreaField('Content', [Required()])
    media_added_ids = TextField('media')
    type_content = SelectField(u'Content Type',
                               [Required()],
                               choices=[('blog', 'Blog Post'),
                                        ('media', 'Lecture'),
                                        ('doc', 'Documentation')]
                               )
    # Comma seprated media id's
    active = BooleanField('Published')
    tags = TextField('Tags', [Required()])
    # Comma seprated tag id's
