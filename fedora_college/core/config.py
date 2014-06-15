#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    FAS_OPENID_ENDPOINT = 'http://id.fedoraproject.org/'
    FAS_CHECK_CERT = True
    DEBUG = False
    TESTING = False
    ADMIN_GROUP = 'provenpackager'
    WHOOSH_BASE = os.path.join(basedir, 'search')


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'FEDORA-DEMO'
    MYSQL_USER = "root"
    MYSQL_PASS = "kgggdkp1992"
    MYSQL_DATABASE = "fedora"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://" + \
        MYSQL_USER + ":" + MYSQL_PASS + "@localhost/" + MYSQL_DATABASE

    SQLALCHEMY_ECHO = True
    DATABASE_CONNECT_OPTIONS = {}
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = "f3do$a"
    UPLOADS_FOLDER = os.path.realpath('.') + '/fedora_college/static/uploads/'
    ALLOWED_EXTENSIONS = {
        'video': ['ogg', 'ogv'],
        'image': ['jpeg', 'png', 'jpg'],
        'doc': ['pdf'],
        'audio': ['mp3', 'flac']
    }


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'FEDORA-TEST'
