# -*- coding: utf-8 -*-
from fedora_college.core.database import db
import datetime

'''
Updated Models / Uploading ER diagram soon.
'''


class Tags(db.Model):
    __tablename__ = 'Tags'

    tag_id = db.Column(db.Integer, primary_key=True)
    tag_text = db.Column(db.String(255))
    date_added = db.Column(db.DateTime())

    def __init__(self, tag_text):
        self.tag_text = tag_text
        self.date_added = datetime.datetime.utcnow()

    def text(self):
        return self.tag_text

    def time(self):
        return self.date_added

    def __repr__(self):
        return '<TagText %r>' % (self.tag_text)


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

    def __repr__(self):
        return '<Username %r>' % (self.username)

    def update(self, open_id=None, username=None,
               email=None, about=None,
               date=None, website=None,
               role=None):
        if open_id is not None:
            self.open_id = open_id
        if username is not None:
            self.username = username
        if email is not None:
            self.email = email
        if about is not None:
            self.about = about
        if date is not None:
            self.date_registered = date
        if website is not None:
            self.website = website
        if role is not None:
            self.role = role

    def name(self):
        return self.username

    def openid(self):
        return self.openid

    def email(self):
        return self.email

    def about(self):
        return self.about

    def website(self):
        return self.website

    def role(self):
        return self.role

    '''
    More methods to be added
    according to usage
    '''


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

    def __repr__(self):
        return '<Media-Title %r>' % (self.title)

    def update(self, title=None, about=None,
               content_url=None, slug=None,
               timestamp=None, tags=None):
        if title is not None:
            self.title = title
        if about is not None:
            self.about = about
        if content_url is not None:
            self.content_url = content_url
        if slug is not None:
            self.slug = slug
        if timestamp is not None:
            self.timestamp = timestamp
        if tags is not None:
            self.tags = tags

    def title(self):
        return self.title

    def about(self):
        return self.about

    def url(self):
        return self.content_url

    def slug(self):
        return self.slug

    def timestamp(self):
        return self.timestamp

    def tags(self):
        return self.tags


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

    def __repr__(self):
        return '<Title %r>' % (self.title)

    def update(self, title=None, slug=None,
               description=None, date_added=None,
               media_added_ids=None,
               active=None, tags=None,
               user_id=None):
        if title is not None:
            self.title = title
        if slug is not None:
            self.slug = slug
        if description is not None:
            self.description = description
        if date_added is not None:
            self.date_added = date_added
        if media_added_ids is not None:
            self.media_added_ids = media_added_ids
        if active is not None:
            self.active = active
        if tags is not None:
            self.tags = tags
        if user_id is not None:
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
    user_id = db.Column(db.Integer, db.ForeignKey(UserProfile.user_id),
                        primary_key=True)
    

    def __init__(self, text, parent, date_added,user_id):
        self.text = text
        self.parent = parent
        self.date_added = date_added
        self.user_id = user_id

    def gettext(self):
        return self.text

    def getparent(self):
        return self.parent

    def getid(self):
        return self.comment_id
        
    def createdby(self):
        return self.user_id

    def date(self):
        return self.date_added

    def __repr__(self):
        return '<Text %r>' % (self.text)


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
    relation = ""

    def __init__(self, comment_id, content_id):
        self.comment_id = comment_id
        self.content_id = content_id
        self.relation = str(comment_id) + " " + str(content_id)

    def __repr__(self):
        return '<Relation %r>' % (self.relation)


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
        return '<Title %s>' % self.title
