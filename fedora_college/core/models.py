#!/usr/bin/env python
# -*- coding: utf-8 -*-
from core.database import db


class Screencast(db.Model):
    __tablename__ = 'screencast'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    desc = db.Column(db.Text)
    date = db.Column(db.Date)

    def __init__(self, name, desc, date):
        self.name = name
        self.desc = desc
        self = date
