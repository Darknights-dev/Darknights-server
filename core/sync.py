#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Sync Data

from bottle import *
import json
import time
import copy

from utils import api, logger, err, file


@route('/u8/pay/getAllProductList', method='POST')
def get_products():
    logger.info("Hit /u8/pay/getAllProductList", request.environ.get('HTTP_X_FORWARDED_FOR'))

    with open('./serverData/AllProductList.json', 'r', encoding='utf-8') as f:
        resp = f.read()
    return json.loads(resp)


@route('/account/syncData', method='POST')
def account_syncData():
    logger.info("Hit /account/syncData", request.environ.get('HTTP_X_FORWARDED_FOR'))

    try:
        secret = request.get_header("secret")
    except BaseException:
        return json.loads(err.badRequestFormat)

    user = api.getUserBySecret(secret)

    if user is None:
        return err.status1

    Ts = api.getTs()
    user = api.completeServerData(user, Ts)
    medium = file.readFile('./template/syncData.json')
    medium = api.loadUserData(user, medium)
    medium = api.updateAllTs(user, medium, Ts)

    # Checkin
    medium['user']['checkIn']['canCheckIn'] = 0

    api.updateUserData(user, medium)

    return medium


@route('/account/syncStatus', method='POST')
def account_syncStatus():
    logger.info("Hit /account/syncStatus", request.environ.get('HTTP_X_FORWARDED_FOR'))

    try:
        secret = request.get_header("secret")
        data = json.loads(request.body.read())
    except BaseException:
        return json.loads(err.badRequestFormat)

    if secret is None:
        return json.loads('{"result":1}')

    user = api.getUserBySecret(secret)

    if user is None:
        return json.loads('{"result":1}')

    Ts = api.getTs()

    # totally no idea what 'modules' means
    if data['modules'] == 7:
        medium = file.readFile('./serverData/syncStatus/7.json')
    elif data['modules'] == 23:
        medium = file.readFile('./serverData/syncStatus/23.json')
    elif data['modules'] == 263:
        medium = file.readFile('./serverData/syncStatus/263.json')
    else:
        medium = file.readFile('./template/syncStatus.json')

    medium['ts'] = Ts
    medium['playerDataDelta']['modified']['status']['lastOnlineTs'] = Ts
    return medium


@route('/building/sync', method='POST')
def building_sync():
    logger.info('Hit /building/sync', request.environ.get('HTTP_X_FORWARDED_FOR'))

    try:
        secret = request.get_header("secret")
    except BaseException:
        return json.loads(err.badRequestFormat)

    if secret is None:
        return json.loads('{"result":1}')
    user = api.getUserBySecret(secret)

    if user is None:
        return json.loads('{"result":1}')

    Ts = api.getTs()

    resp = """
{
    "ts":0,
    "playerDataDelta":{
        "modified":{
            "building":{},
            "event":{
                "building":0
            }
        }
    }
}
    """
    medium = json.loads(resp)
    modify = medium['playerDataDelta']['modified']
    modify['building'] = user['building']
    medium['ts'] = Ts
    modify['building']['status']['labor']['lastUpdateTime'] = Ts
    modify['event']['building'] = Ts + 5455
    return medium
