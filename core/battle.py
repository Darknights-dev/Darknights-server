#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Battle System

from bottle import *
import json

from utils import logger, api, err, encryption


@route('/quest/battleStart', method='POST')
def quest_battleStart():
    """
    Response battle start event, generate a battleId for battleFinish and saveBattleReplay.
    """
    logger.info('Hit /quest/battleStart', request.environ.get('HTTP_X_FORWARDED_FOR'))

    try:
        secret = request.get_header("secret")
        data = json.loads(request.body.read())
        stageId = data['stageId']
        startTs = data['startTs']
    except BaseException:
        return json.loads(err.badRequestFormat)

    if secret is None:
        return json.loads('{"result":1}')

    user = api.getUserBySecret(secret)

    if user is None:
        return json.loads('{"result":1}')

    resp = """
{
    "apFailReturn": 6,
    "battleId": "8f158040-aa62-11eb-9e64-0fd96a7f1bd2",
    "isApProtect": 1,
    "notifyPowerScoreNotEnoughIfFailed": false,
    "playerDataDelta": {
        "deleted": {},
        "modified": {
        }
    },
    "result": 0
}
    """
    medium = json.loads(resp)
    medium['battleId'] = str(user['uid']) + '@' + str(startTs) + '@' + stageId
    return medium


@route('/quest/battleFinish', method='POST')
def quest_battleFinish():
    """
    Response battle finish and rewards.
    """
    logger.info('Hit /quest/battleFinish', request.environ.get('HTTP_X_FORWARDED_FOR'))

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
    resp = """
    {
        "additionalRewards": [],
        "alert": [],
        "apFailReturn": 0,
        "expScale": 1.2,
        "firstRewards": [
            {
                "count": 1,
                "id": "4002",
                "type": "DIAMOND"
            }
        ],
        "furnitureRewards": [],
        "goldScale": 1.2,
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "building": {
                },
                "dexNav": {
                },
                "dungeon": {
                    "stages":{
                    }
                },
                "medal": {
                },
                "mission": {
                },
                "status": {
                },
                "troop": {
                }
            }
        },
        "result": 0,
        "rewards": [
            {
                "count": 0,
                "id": "4001",
                "type": "GOLD"
            }
        ],
        "unlockStages": [],
        "unusualRewards": []
    }
        """
    medium = json.loads(resp)
    # Decryption of battle data
    battle = json.loads(encryption.decrypt_battle_data(data['data'], user['pushFlags']['status']))
    stageId = battle['battleId'].split('@')[2]
    print(battle)
    if battle['interrupt'] == 0 and battle['giveUp'] == 0:
        if battle['percent'] == 100:  # Full success
            medium['playerDataDelta']['modified']['dungeon']['stages'][stageId] = {'state': 3}
            api.update(user, {'status.androidDiamond': user['status']['androidDiamond'] + 1})
            api.update(user, {'dungeon.stages.' + stageId + '.state': 3})
    else:
        medium['firstRewards'] = []
        medium['rewards'] = []

    # Unlock stages needed
    return medium


@route('/quest/saveBattleReplay', method='POST')
def quest_saveBattleReplay():
    """
    Save battle replay.
    """
    logger.info('Hit /quest/saveBattleReplay', request.environ.get('HTTP_X_FORWARDED_FOR'))

    try:
        secret = request.get_header("secret")
        data = json.loads(request.body.read())
        battleId = data['battleId']
        battleReplay = data['battleReplay']
        stageId = battleId.split('@')[2]
    except BaseException:
        return json.loads(err.badRequestFormat)

    if secret is None:
        return json.loads('{"result":1}')

    user = api.getUserBySecret(secret)

    if user is None:
        return json.loads('{"result":1}')

    resp = """
{
    "playerDataDelta": {
        "deleted": {},
        "modified": {
            "dungeon": {
                "stages": {
                }
            }
        }
    },
    "result":0
}
    """
    medium = json.loads(resp)
    medium['playerDataDelta']['modified']['dungeon']['stages'][stageId] = {"hasBattleReplay": 1}
    api.update(user, {
        'battleReplay.' + stageId: battleReplay,
        'dungeon.stages.' + stageId + '.hasBattleReplay': 1
    })
    return medium


@route('/quest/getBattleReplay', method='POST')
def quest_getBattleReplay():
    """
    Get battle replay.
    """
    logger.info('Hit /quest/getBattleReplay', request.environ.get('HTTP_X_FORWARDED_FOR'))

    try:
        secret = request.get_header("secret")
        data = json.loads(request.body.read())
        stageId = data['stageId']
    except BaseException:
        return json.loads(err.badRequestFormat)

    if secret is None:
        return json.loads('{"result":1}')

    user = api.getUserBySecret(secret)

    if user is None:
        return json.loads('{"result":1}')

    resp = """
{
    "battleReplay": "",
     "playerDataDelta": {
        "deleted": {},
        "modified": {}
    }
}
    """
    medium = json.loads(resp)
    medium['battleReplay'] = user['battleReplay'][stageId]
    return medium
