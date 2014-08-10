#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))
''' 
This file houses the config files 
for the whole of the project.
There are 3 types of config.
1. Production : That you may set on Production
2. ProdDemo : for engineerinme.com
3. Development : local testing 
'''


class Config(object):
    FAS_OPENID_ENDPOINT = 'http://id.fedoraproject.org/'
    FAS_CHECK_CERT = True
    ADMIN_GROUP = ['provenpackager', 'summer-coding ']
    # Also, defined in the modules/admin/views.py
    WHOOSH_BASE = os.path.join(basedir, 'search')

    DEBUG = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'fedoracollege@engineerinme.com',
    MAIL_PASSWORD = '********',

    EXTERNAL_URL = "http://demo.engineerinme.com"
    ADMINS = ['hammadhaleem@fedoraproject.org',
              'fedoracollege@engineerinme.com']

    UPLOAD_TOPIC = "fedoracollege.media.upload"
    CONTENT_EDIT_TOPIC = "fedoracollege.content.edit"
    CONTENT_CREATE_TOPIC = "fedoracollege.content.added"

    ALLOWED_EXTENSIONS = {
        'video': ['ogg', 'ogv'],
        'image': ['jpeg', 'png', 'jpg'],
        'doc': ['pdf'],
        'audio': ['mp3', 'flac']
    }

    CSRF_ENABLED = True
    CSRF_SESSION_KEY = "f3do$a"


class ProductionConfig(Config):
    DEBUG = True
    SECRET_KEY = 'FEDORA-DEMO'
    PGSQL_USER = "postgres"
    PGSQL_PASS = "kgggdkp1992"
    PGSQL_DATABASE = "fedora"
    SQLALCHEMY_DATABASE_URI = "postgresql://" + \
        PGSQL_USER + ":" + PGSQL_PASS + "@localhost/" + PGSQL_DATABASE
    SQLALCHEMY_ECHO = False
    DEBUG_TOOLBAR = False
    UPLOADS_FOLDER = '/home/engineer/fedora-college/' + \
        'fedora_college/static/uploads/'
    STATIC_FOLDER = '/home/engineer/fedora-college/fedora_college/static'
    # DEBUG = False
    # TESTING = False
    # DEBUG_TB_PROFILER_ENABLED = False
    # DEBUG_TB_INTERCEPT_REDIRECTS = False


class ProductionConfigDemo(Config):
    DEBUG = True
    SECRET_KEY = 'FEDORA-DEMO'
    PGSQL_USER = "postgres"
    PGSQL_PASS = "kgggdkp1992"
    PGSQL_DATABASE = "fedora"
    SQLALCHEMY_DATABASE_URI = "postgresql://" + \
        PGSQL_USER + ":" + PGSQL_PASS + "@localhost/" + PGSQL_DATABASE

    DEBUG_TOOLBAR = True
    SQLALCHEMY_ECHO = True

    UPLOADS_FOLDER = '/home/engineer/fedora-college/' + \
        'fedora_college/static/uploads/'
    STATIC_FOLDER = '/home/engineer/fedora-college/fedora_college/static'


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'FEDORA-DEMO'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,
                                                          'fedoracollege.db')
    DEBUG_TOOLBAR = True
    SQLALCHEMY_ECHO = True
    DATABASE_CONNECT_OPTIONS = {}
    UPLOADS_FOLDER = os.path.realpath('.') + '/fedora_college/static/uploads/'
    STATIC_FOLDER = os.path.realpath('.') + '/fedora_college/static/'


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'FEDORA-TEST'
