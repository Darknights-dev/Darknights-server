#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Activity System

from bottle import *
import json


@route('/activity/getActivityCheckInReward', method='POST')
def checkIn():
    return json.loads('{"result":0}')


@route('/activity/gridGacha/gacha', method='POST')
def gridGacha():
    return json.loads('{"result":0}')
