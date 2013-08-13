#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Config(object):
    FAS_OPENID_ENDPOINT = 'http://id.fedoraproject.org/'
    FAS_CHECK_CERT = True
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'FEDORA-DEMO'


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'FEDORA-TEST'
