#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Crisis System

from bottle import *
import json

from utils import logger, file


@route('/crisis/getInfo', method='POST')
def crisis_getInfo():
    """
    We need to sync crisis from hypergryph regularly.
    """
    logger.info('Hit /crisis/getInfo', request.environ.get('HTTP_X_FORWARDED_FOR'))

    medium = file.readFile('./serverData/crisis.json')
    medium['ts'] = int(time.time())
    return medium

@route('/crisis/getGoodList', method='POST')
def crisis_getGoodList():
    """
    """
    logger.info('Hit /crisis/getGoodList', request.environ.get('HTTP_X_FORWARDED_FOR'))
    
    medium = file.readFile('./serverData/crisisGoodList.json')
    return medium