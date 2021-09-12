#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Sync Data

from bottle import *
import json
import time

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

    if secret is None:
        return json.loads('{"result":1}')

    user = api.getUserBySecret(secret)

    if user is None:
        return json.loads('{"result":1}')

    Ts = int(time.time())

    medium = file.readFile('./template/syncData.json')
    stageTable = file.readFile('./serverData/stage_table.json')
    

    emptyStage = {
                    "stageId":"",
                    "completeTimes":0,
                    "startTimes":0,
                    "practiceTimes":0,
                    "state":3,
                    "hasBattleReplay":0,
                    "noCostCnt":0
                }
    fullStage = {}
    for i in stageTable['stages'].keys():
        fullStage[i] = emptyStage
        fullStage[i]['stageId'] = i
    # we are using full stage
    medium['user']['dungeon']['stages'] = fullStage

    # Load data from db
    medium['user']['status'] = user['status']
    
    # No difference between android and ios
    medium['user']['status']['iosDiamond'] = medium['user']['status']['androidDiamond']
    
    medium['user']['troop'] = user['troop']
    medium['user']['dexNav']['character'] = user['dexNav']['character']
    medium['user']['building'] = user['building']
    medium['user']['inventory'] = user['inventory']
    medium['user']['status']['lastOnlineTs'] = Ts
    medium['user']['status']['lastRefreshTs'] = Ts
    medium['user']['event']['building'] = Ts
    medium['ts'] = Ts

    medium['user']['checkIn']['canCheckIn'] = 0

    # Experiment zone
    # inventoryList = file.readFile('./serverData/item_table.json')
    # for i in inventoryList['items']:
    # medium['user']['inventory'][i] = 1

    # Update db
    api.update(user, {'status': medium['user']['status']})

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

    Ts = int(time.time())

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

    Ts = int(time.time())

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
