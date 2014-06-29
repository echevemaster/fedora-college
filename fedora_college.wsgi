#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/fedora-college/")

from fedora_college import app as application
application.secret_key = 'Add your secret key'