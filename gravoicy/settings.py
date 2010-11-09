# -*- coding: utf-8 -*-
import os
import sys
import socket
from django.utils.importlib import import_module


PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
CURRENT_HOST = socket.gethostname()
HOST_MAP = {
    'local': 'mark-desktop',
    'server': '',
}
DISPATCHER = []
sys.path.append('%s/apps/' % PROJECT_PATH)
sys.path.append('%s/libs/' % PROJECT_PATH)

def update_settings(config):
    """
    Given a filename, this function will insert all variables and functions
    in ALL_CAPS into the global scope.
    """
    settings = import_module('config.settings_%s' % config)
    for k, v in settings.__dict__.items():
        if k.upper() == k:
            globals().update({k:v})

update_settings('base')

for k, v in HOST_MAP.items():
    if CURRENT_HOST == v:
        DISPATCHER.append(k)

for s in DISPATCHER:
    try:
        update_settings(s)
    except ImportError:
        print "Error importing %s" % s
