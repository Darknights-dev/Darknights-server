#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Shopping System

from bottle import *

import json
import copy
import time

from utils import logger, file, err, api

null = 'null'
true = True
false = False
empty = \
    {
        "playerDataDelta": {
            "deleted": {},
            "modified": {}
        }
    }

_skinTable = file.readFile('./serverData/skin_table.json')
goodTable = file.readFile('./serverData/shop_client_table.json')
skinTable = {}
skinToGood = {}


def skinTableInit():
    for skin in _skinTable['charSkins'].values():
        if skin['isBuySkin']:
            skinTable[skin['skinId']] = skin
    logger.info(str(len(skinTable)) + ' CharSkins Loaded.')


skinTableInit()


@route('/shop/getSkinGoodList', method='POST')
def shop_getSkinGoodList():
    logger.info('Hit /shop/getSkinGoodList', request.environ.get('HTTP_X_FORWARDED_FOR'))

    Ts = api.getTs()
    defaultSkin = {
        "charId": "",
        "currencyUnit": "DIAMOND",
        "desc1": null,
        "desc2": null,
        "discount": 0,
        "endDateTime": -1,
        "goodId": "SS_char_423_blemsh@witch#2",
        "originPrice": 18,
        "price": 18,
        "skinId": "",
        "skinName": "",
        "slotId": 175,
        "startDateTime": -1
    }
    skinList = []
    for i in skinTable.values():
        defaultSkin['charId'] = i['charId']
        defaultSkin['goodId'] = 'SS_' + i['skinId']  # May cause bugs in the future
        defaultSkin['skinId'] = i['skinId']
        defaultSkin['skinName'] = i['displaySkin']['skinName']
        defaultSkin['slotId'] = len(skinList)
        defaultSkin['startDateTime'] = Ts
        defaultSkin['endDateTime'] = Ts + 233333
        skinList.append(copy.deepcopy(defaultSkin))
    medium = json.loads('{"goodList": []}')
    medium['goodList'] = skinList
    return medium


@route('/shop/buySkinGood', method='POST')
def shop_buySkinGood():
    logger.info('Hit /shop/buySkinGood', request.environ.get('HTTP_X_FORWARDED_FOR'))

    try:
        secret = request.get_header("secret")
        data = json.loads(request.body.read())
        goodId = data['goodId']
    except BaseException:
        return json.loads(err.badRequestFormat)

    if secret is None:
        return err.status1

    user = api.getUserBySecret(secret)

    if user is None:
        return err.status1

    Ts = api.getTs()
    skinId = goodId[3:]

    resp = """
{
    "playerDataDelta": {
        "deleted": {},
        "modified": {
            "skin": {
                "characterSkins": {
                },
                "skinTs": {
                }
            }
        }
    }
}
    """
    medium = json.loads(resp)
    modify = medium['playerDataDelta']['modified']
    modify['skin']['characterSkins'] = {skinId: 1}
    modify['skin']['skinTs'] = {skinId: Ts}
    # modify['status']['androidDiamond'] = 0
    api.update(user, {'skin.characterSkins.' + skinId: 1})
    api.update(user, {'skin.skinTs.' + skinId: Ts})
    return medium


@route('/shop/getCashGoodList', method='POST')
def shop_getCashGoodList():
    logger.info('Hit /shop/getCashGoodList', request.environ.get('HTTP_X_FORWARDED_FOR'))

    medium = file.readFile('./serverData/shop/cashGoodList.json')
    return medium


@route('/shop/getGPGoodList', method='POST')
def shop_getGPGoodList():
    logger.info('Hit /shop/getGPGoodList', request.environ.get('HTTP_X_FORWARDED_FOR'))

    medium = file.readFile('./serverData/shop/GPGoodList.json')
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
