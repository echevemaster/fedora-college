# -*- coding: utf-8 -*-
from fedora_college.core.database import db
'''
Updated Models / Uploading ER diagram soon.
'''


'''
class UserProfile(db.Model):
    __tablename__ = 'profile'

    user_id = db.Column(db.Integer, primary_key=True)
    open_id = db.Column(db.String(255))
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    about = db.Column(db.Text())
    date_registered = db.Column(db.DateTime())
    website = db.Column(db.String())

    def __init__(self,open_id,username,email,about,date,website):    
    	self.open_id = open_id
    	self.username = username
    	self.email = email
    	self.about = about
    	self.date_registered = date
    	self.website = website

class Media(db.Model):
    __tablename__ = 'content'

    media_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    about = db.Column(db.Text())
    content_url = db.Column(db.String())
    slug = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime())

    def __init__(self,title,about,url,slug,time):    
    	self.title =title
    	self.about = about
    	self.content_url= url
    	self.slug = slug
    	self.timestamp = time


class Content(db.Model):
    __tablename__ = 'image'

    content_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    description = db.Column(db.Text())
    date_added = db.Column(db.DateTime())
    media_added_ids = db.Column(db.Text())
    active = db.Column(db.Boolean())

    def __init__(self,title,slug,description,date_added,media_added_ids,active):
        self.title = title
        self.slug = slug
        self.description = description
        self.date_added = date_added
	self.media_added_ids=media_added_ids
        self.active = active



class Comments(db.Model):
    __tablename__ = 'comments'
    
    comment_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    parent = db.Column(db.Integer,default=0)
    date_added = db.Column(db.DateTime())
    
    def __init__(self,text,parent,date_added):
        self.text = text
        self.parent = parent
        self.date_added = date_added

class Comment_map_content()	
   __tablename__ = 'map_comments'
    
    comment_id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer)
    
    def __init__(self,comment_id,content_id):
        self.comment_id = comment_id
        self.content_id = content_id

'''
class Screencast(db.Model):
    __tablename__ = 'screencast'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    description = db.Column(db.Text())
    date = db.Column(db.DateTime())
    url_video = db.Column(db.String())
    active = db.Column(db.Boolean())

    def __init__(self, title, slug, description,url_video, date, active):
        self.title = title
        self.slug = slug
        self.description = description
        self.url_video = url_video
        self.date = date
        self.active = active

    def __repr__(self):
        return '<Title %s' % self.title
