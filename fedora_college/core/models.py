# -*- coding: utf-8 -*-
import datetime
import HTMLParser
import uuid
import re
from fedora_college.core.database import db
from flask import (g)


regex = re.compile("\[\[([1-9]*)]\]")

'''
    Database Models
'''


class UserProfile(db.Model):
    __tablename__ = 'profile'

    user_id = db.Column(db.Integer, primary_key=True)
    open_id = db.Column(db.String(255))
    token = db.Column(db.String(1024))
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(500))
    about = db.Column(db.Text())
    date_registered = db.Column(db.DateTime())
    website = db.Column(db.String(255))
    role = db.Column(db.String(50))
    data = {}

    def __init__(self, open_id, username,
                 email, about, website, role):
        self.open_id = open_id
        self.username = username
        self.token = None
        self.email = email
        self.about = about
        self.date_registered = datetime.datetime.utcnow()
        self.website = website
        self.role = role

    def gentoken(self):
            if self.token is None:
                self.token = str(self.username) + '-' + str(uuid.uuid4())
                return self.token
            else:
                return self.token

    def newtoken(self):
        self.token = str(self.username) + '-' + str(uuid.uuid4())
        print self.token
        return self.token

    def getdata(self):
        self.data['user_id'] = self.user_id
        self.data['openid'] = str(self.open_id)
        self.data['username'] = str(self.username)
        self.data['email'] = str(self.email)
        self.data['about'] = str(self.about)
        self.data['member-since'] = str(self.date_registered)
        self.data['website'] = str(self.website)
        self.data['role'] = str(self.role)

        return self.data

    def __repr__(self):
        return '<Username %r>' % (self.username)

    def getMedia(self):
        '''
            return all media added by user
        '''
        try:
            media = Media.query.filter_by(
                user_id=g.fas_user['username']).first()
            return media
        except:
            media = None
            return None

    def getContent(self):
        '''
            return all content written by user
        '''
        try:
            content = Content.query.filter_by(
                user_id=g.fas_user['username']).first()
            return content
        except:
            content = None
            return None

    '''
    More methods to be added
    according to usage
    '''


class Media(db.Model):
    __tablename__ = 'media'
    __searchable__ = ['featured_name', 'tags']

    media_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(2024))
    content_url = db.Column(db.String(2024))
    sys_path = db.Column(db.String(2024))
    timestamp = db.Column(db.DateTime())
    file_type = db.Column(db.String(255))
    user_id = db.Column(db.String(255), db.ForeignKey(UserProfile.username))
    revise = db.Column(db.Text())
    thumb_url = db.Column(db.String(2024))
    tags = db.Column(db.String(2024))
    featured_name = db.Column(db.String(2024))

    def process_tags(self, text):
        stri = text.split(",")
        ret = ""
        for i in stri:
            ret = ret + str(i) + " "
        return ret

    def __init__(self, filename, sys_path, url,
                 user_id, types, thumb_url,
                 tags, featured_name
                 ):
        self.name = filename
        self.content_url = url
        self.sys_path = sys_path
        self.user_id = user_id
        self.timestamp = datetime.datetime.utcnow()
        self.file_type = types
        self.revise = "{}"
        self.thumb_url = thumb_url
        self.tags = self.process_tags(tags)
        self.featured_name = featured_name

    def getdata(self):
        data = dict()
        data['id'] = str(self.media_id)
        data['filename'] = str(self.name)
        data['content_url'] = str(self.content_url)
        data['sys_path '] = str(self.sys_path)
        data['timestamp'] = str(self.timestamp)
        data['thumb'] = str(self.thumb_url)
        data['file_type'] = str(self.file_type)
        data['tags'] = str(self.tags)
        data['name'] = str(self.featured_name)
        return data

    def __repr__(self):
        return '<Media-Title %r>' % (self.media_id)


class Content(db.Model):
    __tablename__ = 'content'
    __searchable__ = ['title', 'description']

    """
    This class stores information about the Content
    """

    content_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    slug = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text())
    html = db.Column(db.Text())
    date_added = db.Column(db.DateTime())
    media_added_ids = db.Column(db.Text())
    type_content = db.Column(db.String(255))
    # Comma seprated media id's
    active = db.Column(db.Boolean())
    # Comma seprated tag id's
    tags = db.Column(db.Text())
    user_id = db.Column(db.String(255), db.ForeignKey(UserProfile.username))
    thumb_url = db.Column(db.String(2024))

    def gethtml(self, media_id):
        data = Media.query.filter_by(media_id=media_id).first_or_404()

        if data is not None:
            url = data.content_url
            if data.file_type == "image":
                html = "<img src='/" + url + "' />"
            if data.file_type == "video":
                html = "<video width='auto'  controls>"
                html = html + "<source src='" + url + "' type='video/ogg'>"
                html = html + "Your browser does not support the video tag."
                html = html + "</video>"
            return html
        else:
            return None

    def admedia(self, text):
        out = regex.findall(text)
        ids = ""
        for i in out:
            if self.gethtml(i) is not None:
                text = text.replace("[[" + str(i) + "]]", self.gethtml(i))
            else:
                text = text.replace("[[" + str(i) + "]]", " ")
            ids = ids + i + ","

        return text, ids, out[0]

    def __init__(self, title, slug, description,
                 active, tags, user_id,
                 type_content="blog"):
        self.title = title
        self.slug = slug
        self.description = description
        self.date_added = datetime.datetime.utcnow()
        self.active = active
        self.type_content = type_content
        self.tags = tags
        self.user_id = user_id
        self.html, self.media_added_ids, ids = self.admedia(description)
        feature = Media.query.filter_by(media_id=ids).first_or_404()
        self.thumb_url = feature.thumb_url

    def rehtml(self):
        self.html, self.media_added_ids, ids = self.admedia(self.description)
        feature = Media.query.filter_by(media_id=ids).first_or_404()
        self.thumb_url = feature.thumb_url

    def getdata(self):
        data = {}
        data['id'] = self.content_id
        data['title'] = self.title
        data['slug'] = self.slug
        data['description'] = self.description
        data['date_added'] = self.date_added
        data['media_added_ids'] = self.media_added_ids
        data['type'] = self.type_content
        data['active'] = self.active
        data['tags'] = self.tags
        data['user_name'] = self.user_id
        return data

    def tohtml(self):
        ret = HTMLParser.HTMLParser()
        ret = ret.unescape(self.description)
        return ret

    def __repr__(self):
        return '<Title %r>' % (self.title)


class Tags(db.Model):
    __tablename__ = 'tags'

    tag_id = db.Column(db.Integer, primary_key=True)
    tag_text = db.Column(db.String(255))
    date_added = db.Column(db.DateTime())

    def __init__(self, tag_text):
        self.tag_text = tag_text
        self.date_added = datetime.datetime.utcnow()

    def __repr__(self):
        return '<TagText %r>' % (self.tag_text)

    def getdata(self):
        return {
            "id": self.tag_id,
            "text": self.tag_text,
            "created": self.date_added
        }


class TagsMap(db.Model):
    __tablename__ = 'tagsmap'

    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey(Tags.tag_id))
    content_id = db.Column(db.Integer, db.ForeignKey(Content.content_id))

    def __init__(self, tag_id, content_id):
        self.tag_id = tag_id
        self.content_id = content_id

    def __repr__(self):
        return '<TagText %r>' % (self.tag_text)

    def getdata(self):
        return {
            "tag_id": self.tag_id,
            "content_id": self.content_id,
            "id": self.id
        }


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

    def __repr__(self):
        return '<Text %r>' % (self.text)


class Comment_map_content(db.Model):
    __tablename__ = 'commentsmap'

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
