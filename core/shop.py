#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Shopping System

from bottle import *
import json
from utils import logger, file


@route('/shop/getSkinGoodList', method='POST')
def shop_getSkinGoodList():
    logger.info('Hit /shop/getSkinGoodList', request.environ.get('HTTP_X_FORWARDED_FOR'))

    medium = file.readFile('./serverData/shop/skinGoodList.json')
    return medium


@route('/shop/getCashGoodList', method='POST')
def shop_getCashGoodList():
    logger.info('Hit /shop/getCashGoodList', request.environ.get('HTTP_X_FORWARDED_FOR'))

    medium = file.readFile('./serverData/shop/cashGoodList.json')
    return medium


@route('/shop/getGoodPurchaseState', method='POST')
def shop_getGoodPurchaseState():
    logger.info('Hit /shop/getGoodPurchaseState', request.environ.get('HTTP_X_FORWARDED_FOR'))
    resp = """
{
    "playerDataDelta": {
        "deleted": {},
        "modified": {}
    },
    "result": {}
}
    """
    medium = json.loads(resp)
    return medium
