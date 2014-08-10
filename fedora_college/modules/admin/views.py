# -*- coding: utf-8 -*-
from flask import g
from flask.ext import admin
from flask.ext.admin.contrib import sqla
from flask.ext.admin import expose
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask import current_app
admins = set(current_app.config['ADMIN_GROUP'])
groups = set(list(g.fas_user['groups']))
# Create customized index view
# class that handles login & registration
# Each of the associated view has an
# attached accessible efunction defined.
# View for fedora admin models


class FedoraModelView(sqla.ModelView):
    column_display_pk = True
    column_display_pk = True

    def is_accessible(self):
        try:
            if admin & groups:
                return True
            else:
                return False
        except:
            return False

# view for  fedora file models


class FedoraFileView(FileAdmin):

    def is_accessible(self):
        try:
            if admin & groups
                return True
            else:
                return False
        except:
            return False

# View for the index page of fedora admin


class FedoraAdminIndexView(admin.AdminIndexView):

    column_display_pk = True
    column_display_fk = True

    def is_accessible(self):
        try:
            if admin & groups
                return True
            else:
                return False
        except:
            return False

    @expose('/')
    def index(self):
        try:
            if g.fas_user.username:
                return super(FedoraAdminIndexView, self).index()
            return str(self.is_accessible())
        except:
            return "404"
