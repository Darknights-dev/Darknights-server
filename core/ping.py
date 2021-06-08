#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Useless Ping

from bottle import *
import json

from utils import *


@route('/beat', method='POST')
def beat():
    return json.loads('{"code":200,"msg":"ok","next":36000}')


@route('/online/v1/loginout', method='POST')
def online_v1_loginout():
    return json.loads('{"result":0}')


@route('/u/g/v1/<n>', method='POST')
def statistics(n):
    return "ok"


@route('/v1/<n>', method='POST')
def statistics(n):
    return "ok"


@route('/event', method='POST')
def event():
    resp = """
{
    "code": 200,
    "msg": "ok"
}
    """
    return json.loads(resp)


@route('/online/v1/ping', method='POST')
def online_ping():
    resp = """
{
    "alertTime": 600,
    "interval": 3590,
    "message": "OK",
    "result": 0,
    "timeLeft": -1
}
    """
    return json.loads(resp)
