#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Char Build System

from bottle import *
import json
import time

from utils import logger, api, err, file

with open('./serverData/gamedata_const.json', 'r', encoding='utf-8') as f:
    constConfig = json.loads(f.read())
    logger.info('Constant Gamedata Loaded.')

with open('./serverData/character_table.json', 'r', encoding='utf-8') as f:
    characterTable = json.loads(f.read())

@route('/charBuild/boostPotential', method='POST')
def charBuild_boostPotential():
    logger.info('Hit /charBuild/boostPotential',
                request.environ.get('HTTP_X_FORWARDED_FOR'))

    try:
        secret = request.get_header("secret")
        data = json.loads(request.body.read())
        charInstId = data['charInstId']
        targetRank = data['targetRank']
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
            "inventory": {
                "p_char_187_ccheal": 0
            },
            "troop": {
                "chars": {
                    "0": {
                        "potentialRank": 1
                    }
                }
            }
        }
    },
    "result": 1
}
    """
    medium = json.loads(resp)
    modify = medium['playerDataDelta']['modified']
    modify['inventory'] = {}
    modify['troop']['chars'] = json.loads(
        '{"' + str(charInstId) + '":{"potentialRank":' + str(targetRank) + '}}')
    return medium


@route('/charBuild/upgradeChar', method='POST')
def charBuild_upgradeChar():
    logger.info('Hit /charBuild/upgradeChar',
                request.environ.get('HTTP_X_FORWARDED_FOR'))

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

    curChar = user['troop']['chars'][str(data['charInstId'])]
    curExp = curChar['exp']
    curLevel = curChar['level']
    expDelta = 0

    for item in data['expMats']:
        if item['id'] == '2004':
            expDelta = expDelta + 2000 * item['count']
        elif item['id'] == '2003':
            expDelta = expDelta + 1000 * item['count']
        elif item['id'] == '2002':
            expDelta = expDelta + 400 * item['count']
        else:
            expDelta = expDelta + 200 * item['count']

    Phase = curChar['evolvePhase']

    expNow = curExp + expDelta

    levelNew = 0
    expCost = 0

    for i in range(curLevel - 1, len(constConfig['characterExpMap'][Phase])):
        if(expCost + abs(constConfig['characterExpMap'][Phase][i]) > expNow):
            levelNew = i + 1
            exp = expNow - expCost
            break
        else:
            expCost = expCost + constConfig['characterExpMap'][Phase][i]

    maxLevel = constConfig['maxLevel'][characterTable[curChar['charId']]["rarity"]][curChar['evolvePhase']]
    if levelNew >= maxLevel:
        levelNew = maxLevel
        exp = 0
    gold = user['status']['gold']
    goldCost = 0

    if curLevel == levelNew:
        goldCost = round(((exp - curExp) / constConfig['characterExpMap'][Phase][curLevel - 1]) * constConfig['characterUpgradeCostMap'][Phase][curLevel - 1]) 
    elif levelNew == curLevel + 1:
        goldCost = round((((constConfig['characterExpMap'][Phase][curLevel - 1] - curExp) / constConfig['characterExpMap'][Phase][curLevel - 1]) * constConfig['characterUpgradeCostMap'][Phase][curLevel - 1])
                        +(( exp / constConfig['characterExpMap'][Phase][levelNew - 1]) * constConfig['characterUpgradeCostMap'][Phase][levelNew - 1]))
    else:
        for i in range(curLevel + 1 - 1, levelNew - 1 - 1 + 1):
            goldCost = goldCost + constConfig['characterUpgradeCostMap'][Phase][i]
        goldCost = goldCost +  round((((constConfig['characterExpMap'][Phase][curLevel - 1] - curExp) / constConfig['characterExpMap'][Phase][curLevel - 1]) * constConfig['characterUpgradeCostMap'][Phase][curLevel - 1])
                        +(( exp / constConfig['characterExpMap'][Phase][levelNew - 1]) * constConfig['characterUpgradeCostMap'][Phase][levelNew - 1]))

    gold = gold - goldCost

    resp = """
    {
    "playerDataDelta": {
        "modified": {
            "inventory": {
                "2001": 100
            },
            "troop": {
                "chars": {

                }
            },
            "status": {
                "gold": 103610
            }
        },
        "deleted": {}
    }
}
"""
    medium = json.loads(resp)
    api.update(user, {'troop.chars.' + str(data['charInstId']) + '.exp': exp,
                      'troop.chars.' + str(data['charInstId']) + '.level': levelNew,
                      'status.gold': gold})
    for i in data['expMats']:
        medium['playerDataDelta']['modified']['inventory'][i['id']] = user['inventory'][i['id']] - i['count']
        api.update(user,{'inventory.' + i['id']:user['inventory'][i['id']] - i['count']})
    medium['playerDataDelta']['modified']['troop']['chars'] = {
        str(data['charInstId']): {'exp': exp, 'level': levelNew}}
    medium['playerDataDelta']['modified']['status']['gold'] = gold
    return medium


@route('/charBuild/changeCharSkin', method='POST')
def charBuild_changeCharSkin():
    logger.info('Hit /charBuild/changeCharSkin',
                request.environ.get('HTTP_X_FORWARDED_FOR'))

    try:
        secret = request.get_header("secret")
        data = json.loads(request.body.read())
        charInstId = data['charInstId']
        skinId = data['skinId']
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
            "troop": {
                "chars": {
                    "0": {
                        "skin": "char_102_texas#1"
                    }
                }
            }
        }
    }
}
    """
    medium = json.loads(resp)
    medium['playerDataDelta']['modified']['troop']['chars'][str(charInstId)] = {
        "skin": skinId}
    return medium


@route('/charBuild/evolveChar', method='POST')
def charBuild_evolveChar():
    return


@route('/charBuild/batchSetCharVoiceLan', method='POST')
def charBuild_batchSetCharVoiceLan():
    medium = file.readFile('./template/voiceSettings.json')
    return medium
