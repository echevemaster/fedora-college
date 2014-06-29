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
    DEBUG_TB_PROFILER_ENABLED = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'FEDORA-DEMO'
    PGSQL_USER = "postgres"
    PGSQL_PASS = "kgggdkp1992"
    PGSQL_DATABASE = "fedora"
    '''
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,
                                                          'fedoracollege.db')
    '''
    SQLALCHEMY_DATABASE_URI = "postgresql://" + \
        PGSQL_USER + ":" + PGSQL_PASS + "@localhost/" + PGSQL_DATABASE
    SQLALCHEMY_ECHO = True
    DATABASE_CONNECT_OPTIONS = {}
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = "f3do$a"
    UPLOADS_FOLDER = os.path.realpath('.') + '/fedora_college/static/uploads/'
    STATIC_FOLDER = os.path.realpath('.') + '/fedora_college/static/'
    ALLOWED_EXTENSIONS = {
        'video': ['ogg', 'ogv'],
        'image': ['jpeg', 'png', 'jpg'],
        'doc': ['pdf'],
        'audio': ['mp3', 'flac']
    }


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'FEDORA-TEST'
