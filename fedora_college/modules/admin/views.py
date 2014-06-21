#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.admin import Admin, BaseView, expose


class MyView(BaseView):

    def is_accessible(self):
        return login.current_user.is_authenticated()

    @expose('/')
    def index(self):
        return self.render('index.html')
