import os
from flask import Flask, url_for, redirect, render_template, request, g
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import form, fields, validators
from flask.ext import admin, login
from flask.ext.admin.contrib import sqla
from flask.ext.admin import helpers, expose


from flask.ext.admin.contrib.fileadmin import FileAdmin

# Create customized index view class that handles login & registration


class FedoraModelView(sqla.ModelView):

    def is_accessible(self):
        try:
            groups = list(g.fas_user['groups'])
            if len(groups) > 0:
                return True
            else:
                return False
        except Exception as e:
            return False


class FedoraFileView(FileAdmin):

    def is_accessible(self):
        try:
            groups = list(g.fas_user['groups'])
            if len(groups) > 0:
                return True
            else:
                return False
        except Exception as e:
            return False


class FedoraAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        try:
            if g.fas_user.username:
                return super(FedoraAdminIndexView, self).index()
            return str(is_accessible())
        except:
            return "404"
