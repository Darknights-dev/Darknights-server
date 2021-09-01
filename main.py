#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Conjecture is impossible. You have the right to reject this story.

import os
import json

from bottle import *

from core import *
from utils import logger

base_path = os.path.dirname(os.path.realpath(__file__))  # base dir
listen_port = 9443  # handle all ak server
domain_name = "example.com"

HTML = \
    """
    Great ideals but through selfless struggle and sacrifice to achieve.
    """


# EntryPoint
@route('/')
@route('/index.html')
def index():
    return HTML


@route('/announce/IOS/preannouncement.meta.json')
@route('/announce/Android/preannouncement.meta.json')
def ann():
    resp = """
{
    "actived": true,
    "preAnnounceId": 280,
    "preAnnounceType": 2,
    "preAnnounceUrl": ""
}
    """
    medium = json.loads(resp)
    medium['preAnnounceUrl'] = "https://" + domain_name + "/announce/Android/preannouncement/280.html"
    return medium


@route('/announce/Android/preannouncement/280.html')
@route('/announce/IOS/preannouncement/280.html')
def announce():
    return HTML


# Handle Error
@error(404)
def error404(error):
    logger.info(str(error), request.environ.get('HTTP_X_FORWARDED_FOR'))
    print(error)
    return "404 Not Found"


@error(500)
def error500(error):
    logger.info(str(error), request.environ.get('HTTP_X_FORWARDED_FOR'))
    return '500 Internal Error'


run(
    host='0.0.0.0',
    server='gunicorn',
    debug=True,
    port=listen_port,
    reloader=True,
    keyfile='./cert/key.pem',
    certfile='./cert/cert.pem'
)