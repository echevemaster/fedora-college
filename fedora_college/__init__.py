#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":mod:`fedora_college` -- A virtual learning environment for Fedora
"""
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import fedora_college

from fedora_college import metadata


__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright

