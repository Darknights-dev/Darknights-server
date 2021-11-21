#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Crisis System

from bottle import *

from utils import logger, file, api

import json


@route('/crisis/getInfo', method='POST')
def crisis_getInfo():
    """
    We need to sync crisis from hypergryph regularly.
    """
    logger.info('Hit /crisis/getInfo', request.environ.get('HTTP_X_FORWARDED_FOR'))

    medium = file.readFile('./serverData/crisis.json')
    medium['ts'] = api.getTs()
    return medium


@route('/crisis/getGoodList', method='POST')
def crisis_getGoodList():
    """
    """
    logger.info('Hit /crisis/getGoodList', request.environ.get('HTTP_X_FORWARDED_FOR'))

    medium = file.readFile('./serverData/crisisGoodList.json')
    return medium


@route('/crisis/battleStart', method='POST')
def crisis_battleStart():
    """
    No solution now.
    """
    logger.info('Hit /crisis/battleStart', request.environ.get('HTTP_X_FORWARDED_FOR'))
    data = """
    {
    "battleId": "",
    "playerDataDelta": {
        "deleted": {},
        "modified": {}
    },
    "result": 0,
    "sign": "",
    "signStr": ""
    }
    """
    medium = json.loads(data)
    return medium
