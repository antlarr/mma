# -*- coding: utf-8 -*-
import os
import re
import json
import pwd


def readConfiguration():
    cfgfile = os.path.expanduser('~/.config/bard')
    if not os.path.isfile(cfgfile):
        raise FileNotFoundError('Configuration file not found.'
                                'Please configure the application at %s'
                                % cfgfile)

    data = ''.join([line for line in open(cfgfile).readlines()
                    if not re.match(r'\s*(#|//)', line)])

    return json.loads(data)


config = readConfiguration()

if 'username' not in config:
    config['username'] = pwd.getpwuid(os.getuid()).pw_name

if 'immutableDatabase' not in config:
    config['immutableDatabase'] = False


def translatePath(path):
    if config['translatePaths']:
        for (src, tgt) in config['pathTranslationMap']:
            src = src.rstrip('/')
            tgt = tgt.rstrip('/')
            if path.startswith(src):
                return tgt + path[len(src):]
    return path
