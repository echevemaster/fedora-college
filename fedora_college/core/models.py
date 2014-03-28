# -*- coding: utf-8 -*-
from fedora_college.core.database import db
'''
Updated Models / Uploading ER diagram soon.
'''


class Tags(db.Model):
    __tablename__ = 'Tags'

    tag_id = db.Column(db.Integer, primary_key=True)
    tag_text = db.Column(db.String(255))
    date_added = db.Column(db.DateTime())

    def __init__(self, tag_text, date_added):
        self.tag_text = tag_text
        self.date_added = date_added


class UserProfile(db.Model):
    __tablename__ = 'profile'

    user_id = db.Column(db.Integer, primary_key=True)
    open_id = db.Column(db.String(255))
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    about = db.Column(db.Text())
    date_registered = db.Column(db.DateTime())
    website = db.Column(db.String())
    role = db.Column(db.Integer)

    def __init__(self, open_id, username,
                 email, about, date, website, role):
        self.open_id = open_id
        self.username = username
        self.email = email
        self.about = about
        self.date_registered = date
        self.website = website
        self.role = role


class Media(db.Model):
    __tablename__ = 'content'

    media_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    about = db.Column(db.Text())
    content_url = db.Column(db.String())
    slug = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime())
    tags = db.Column(db.Text())
    # Comma seprated tag id's

    def __init__(self, title, about, url, slug, time, tags):
        self.title = title
        self.about = about
        self.content_url = url
        self.slug = slug
        self.timestamp = time
        self.tags = tags


class Content(db.Model):
    __tablename__ = 'image'

    """
    This class stores information about the Content
    """

    content_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    description = db.Column(db.Text())
    date_added = db.Column(db.DateTime())
    media_added_ids = db.Column(db.Text())
    # Comma seprated media id's
    active = db.Column(db.Boolean())
    tags = db.Column(db.Text())
    # Comma seprated tag id's
    media = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey(UserProfile.user_id),
                        primary_key=True)

    def __init__(self, title, slug, description, date_added,
                 media_added_ids, active, tags, user_id):
        self.title = title
        self.slug = slug
        self.description = description
        self.date_added = date_added
        self.media_added_ids = media_added_ids
        self.active = active
        self.tags = tags
        self.user_id = user_id


class Comments(db.Model):
    __tablename__ = 'comments'

    """
    Store comment text and relationships
    """

    comment_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    parent = db.Column(db.Integer, default=0)
    date_added = db.Column(db.DateTime())

    def __init__(self, text, parent, date_added):
        self.text = text
        self.parent = parent
        self.date_added = date_added


class Comment_map_content(db.Model):
    __tablename__ = 'map_comments'

    """
    Will be used as relationship table to
    map comments to media or content Items
    """

    comment_id = db.Column(db.Integer, db.ForeignKey(Comments.comment_id),
                           primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey(Content.content_id),
                           primary_key=True)

    def __init__(self, comment_id, content_id):
        self.comment_id = comment_id
        self.content_id = content_id

"""
   From old schema. Removal may cause
   breaking of application would
   be removed soon
"""


class Screencast(db.Model):
    __tablename__ = 'screencast'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    description = db.Column(db.Text())
    date = db.Column(db.DateTime())
    url_video = db.Column(db.String())
    active = db.Column(db.Boolean())

    def __init__(self, title, slug, description,
                 url_video, date, active):
        self.title = title
        self.slug = slug
        self.description = description
        self.url_video = url_video
        self.date = date
        self.active = active

    def __repr__(self):
        return '<Title %s' % self.title
