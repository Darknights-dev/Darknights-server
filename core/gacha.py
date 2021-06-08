#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Gacha System

import json
import random
import time

from bottle import *

from utils import file, logger, api, err

false = 'false'
true = 'true'
null = 'null'

# Load chars from char table
with open('./serverData/character_table.json', 'r', encoding='utf-8') as f:
    fullCharList = eval(f.read())
    fullCharName = []
    for i in fullCharList:
        if fullCharList[i]['isNotObtainable'] == false:
            if i.startswith('char'):
                fullCharName.append(i)

logger.info(str(len(fullCharName)) + ' operators loaded.')

# this will be replaced with ./serverData/pool/xxx
oneGachaCost = 600


@route('/gacha/syncNormalGacha', method='POST')
def gacha_syncNormalGacha():
    """
    Sync
    """
    logger.info('Hit /gacha/syncNormalGacha', request.environ.get('HTTP_X_FORWARDED_FOR'))

    medium = file.readFile('./template/syncNormalGacha.json')
    return medium


@route('/gacha/finishNormalGacha', method='POST')
def gacha_finishNormalGacha():
    logger.info('Hit /gacha/finishNormalGacha', request.environ.get('HTTP_X_FORWARDED_FOR'))

    data = json.loads(request.body.read())
    medium = file.readFile('./template/finishNormalGacha.json')
    return medium


@route('/gacha/advancedGacha', method='POST')
def gacha_advancedGacha():
    logger.info('Hit /gacha/advancedGacha', request.environ.get('HTTP_X_FORWARDED_FOR'))

    try:
        secret = request.get_header("secret")
    except BaseException:
        return json.loads(err.badRequestFormat)

    if secret is None:
        return json.loads('{"result":1}')
    user = api.getUserBySecret(secret)

    if user is None:
        return json.loads('{"result":1}')

    diamondShard = user['status']['diamondShard']
    lggShard = user['status']['lggShard']

    if diamondShard - oneGachaCost < 0:
        return json.loads('{"result":1}')

    """
    charInstId saved in user['troop']['chars']
    charName saved in user['dexNav']['character']
    Do not forget to modify building.
    """
    Ts = int(time.time())

    curCharInstId = user['troop']['curCharInstId']
    charId = random.randint(0, len(fullCharName) - 1)
    charGet = fullCharName[charId]
    isNew = 1
    if charGet in user['dexNav']['character']:
        isNew = 0
        instId = user['dexNav']['character'][charGet]['charInstId']
    else:
        instId = curCharInstId

    # Construct Char Info
    charNew = {
        str(instId): {
            "instId": instId,
            "charId": charGet,
            "favorPoint": 0,
            "potentialRank": 0,
            "mainSkillLvl": 1,
            "skin": charGet + "#1",
            "level": 1,
            "exp": 0,
            "evolvePhase": 0,
            "defaultSkillIndex": 0,
            "gainTime": Ts,
            "skills": []
        }
    }

    for skill in fullCharList[charGet]['skills']:
        skillNew = {
            "skillId": skill['skillId'],
            "unlock": 1,
            "state": 0,
            "specializeLevel": 0,
            "completeUpgradeTime": -1
        }
        charNew[str(instId)]['skills'].append(skillNew)

    resp = """
{
    "charGet":{
        "charId":"",
        "charInstId":0,
        "isNew":1,
        "itemGet":[
            {
                "count":1,
                "id":"4004",
                "type":"HGG_SHD"
            }
        ]
    },
    "playerDataDelta":{
        "modified":{
            "building":{
                "chars":{}
            },
            "dexNav":{
                "character":{
                }
            },
            "inventory":{
            },
            "status":{
                "diamondShard":0,
                "lggShard":0
            },
            "troop":{
                "chars":{
                },
                "charGroup":{
                },
                "curCharInstId":0
            }
        }
    },
    "result":0
}
"""
    medium = json.loads(resp)
    medium['charGet']['charId'] = charGet
    medium['charGet']['charInstId'] = instId
    medium['charGet']['isNew'] = isNew
    medium['charGet']['itemGet'].append({
        'count': 1,
        'id': "p_" + charGet,
        'type': 'MATERIAL'
    })

    modify = medium['playerDataDelta']['modified']

    modify['inventory']['p_' + charGet] = 1

    modify['status']['diamondShard'] = diamondShard - oneGachaCost
    modify['status']['lggShard'] = lggShard + 10

    # New Char Get
    if isNew:
        newCharBuilding = {
            "charId": charGet,
            "lastApAddTime": Ts,
            "ap": 8640000,
            "roomSlotId": "",
            "index": -1,
            "changeScale": 0,
            "bubble": {
                "normal": {
                    "add": -1,
                    "ts": 0
                },
                "assist": {
                    "add": -1,
                    "ts": 0
                }
            },
            "workTime": 0
        }
        modify['troop']['chars'][str(instId)] = charNew[str(instId)]
        modify['troop']['charGroup'][charGet] = {"favorPoint": 0}
        modify['troop']['curCharInstId'] = instId + 1
        modify['dexNav']['character'][charGet] = {'charInstId': instId, 'count': 1}
        modify['building']['chars'][str(instId)] = newCharBuilding
        api.update(user, {
            'dexNav.character.' + charGet: {
                'charInstId': instId,
                'count': 1
            },
            'troop.chars.' + str(instId): charNew[str(instId)],
            'troop.charGroup.' + charGet: {"favorPoint": 0},
            'troop.curCharInstId': instId + 1,
            'building.chars' + str(instId): newCharBuilding,
            'inventory.' + "p_" + charGet: 1
        })
    else:
        api.update(user, {
            'inventory.' + "p_" + charGet: user['inventory']['p_' + charGet] + 1
        })
    # Subtract
    api.update(user, {
        'status.lggShard': lggShard + 10,
        'status.diamondShard': diamondShard - oneGachaCost
    })

    return medium


@route('/gacha/tenAdvancedGacha', method='POST')
def gacha_tenAdvancedGacha():
    logger.info('Hit /gacha/tenAdvancedGacha', request.environ.get('HTTP_X_FORWARDED_FOR'))

    try:
        secret = request.get_header("secret")
    except BaseException:
        return json.loads(err.badRequestFormat)

    if secret is None:
        return json.loads('{"result":1}')
    user = api.getUserBySecret(secret)

    if user is None:
        return json.loads('{"result":1}')

    if user['status']['diamondShard'] - 10 * oneGachaCost < 0:
        return json.loads('{"result":1}')

    Ts = int(time.time())

    gachaResultList = []  # gacha result, all chars directly send back
    instIdResult = {}  # save generated char's instId
    newCharList = {}  # real NEW char
    inventory = {}  # char's inventory

    curCharInstId = user['troop']['curCharInstId']

    for num in range(10):
        charId = random.randint(0, len(fullCharName) - 1)
        charGet = fullCharName[charId]

        isNew = 1
        if charGet in user['dexNav']['character']:  # if char was gotten
            isNew = 0
            instId = user['dexNav']['character'][charGet]['charInstId']
        elif charGet in instIdResult:  # if char is being gotten
            isNew = 0
            instId = instIdResult[charGet]
        else:
            instId = curCharInstId
            instIdResult[charGet] = instId
            curCharInstId = curCharInstId + 1  # real NEW char
        if isNew == 1:
            charNew = {
                "instId": instId,
                "charId": charGet,
                "favorPoint": 0,
                "potentialRank": 0,
                "mainSkillLvl": 1,
                "skin": charGet + "#1",
                "level": 1,
                "exp": 0,
                "evolvePhase": 0,
                "defaultSkillIndex": 0,
                "gainTime": Ts,
                "skills": []
            }

            for skill in fullCharList[charGet]['skills']:
                skillNew = {
                    "skillId": skill['skillId'],
                    "unlock": 1,
                    "state": 0,
                    "specializeLevel": 0,
                    "completeUpgradeTime": -1
                }
                charNew['skills'].append(skillNew)

                newCharList[str(instId)] = charNew

        gachaResultList.append(
            {
                'charId': charGet,
                'charInstId': instId,
                'isNew': isNew,
                'itemGet': [
                    {
                        "count": 1,
                        "id": "4004",
                        "type": "HGG_SHD"
                    },
                    {
                        'count': 1,
                        'id': "p_" + charGet,
                        'type': 'MATERIAL'
                    }
                ]
            }

        )
        inv = "p_" + charGet
        if inv in user['inventory']:
            inventory[inv] = user['inventory'][inv] + 1
        else:
            inventory[inv] = 1

    resp = """
    {
        "gachaResultList":[],
        "playerDataDelta":{
            "modified":{
                "building":{
                    "chars":{}
                },
                "dexNav":{
                    "character":{
                    }
                },
                "inventory":{
                },
                "status":{
                    "diamondShard":0,
                    "lggShard":0
                },
                "troop":{
                    "chars":{
                    },
                    "charGroup":{
                    },
                    "curCharInstId":0
                }
            }
        },
        "result":0
    }
        """
    medium = json.loads(resp)
    medium['gachaResultList'] = gachaResultList

    modify = medium['playerDataDelta']['modified']
    modify['inventory'] = inventory
    modify['status']['diamondShard'] = user['status']['diamondShard'] - 10 * oneGachaCost
    modify['status']['lggShard'] = user['status']['lggShard'] + 10 * 10
    api.update(user, {
        'status.lggShard': user['status']['lggShard'] + 10 * 10,
        'status.diamondShard': user['status']['diamondShard'] - 10 * oneGachaCost,
        'troop.curCharInstId': curCharInstId
    })
    modify['troop']['curCharInstId'] = curCharInstId  # finish all gacha
    for newChar in newCharList:
        newCharId = newCharList[newChar]['charId']
        newCharInstId = newCharList[newChar]['instId']
        modify['dexNav']['character'][newCharId] = {'charInstId': newCharInstId, 'count': 1}
        newCharBuilding = {
            "charId": newCharId,
            "lastApAddTime": Ts,
            "ap": 8640000,
            "roomSlotId": "",
            "index": -1,
            "changeScale": 0,
            "bubble": {
                "normal": {
                    "add": -1,
                    "ts": 0
                },
                "assist": {
                    "add": -1,
                    "ts": 0
                }
            },
            "workTime": 0
        }
        modify['building']['chars'][str(newCharInstId)] = newCharBuilding
        modify['troop']['charGroup'][newCharId] = {"favorPoint": 0}
        modify['troop']['chars'][str(newCharInstId)] = newCharList[newChar]
        """
                charNew = {
                    "instId": instId,
                    "charId": charGet,
                    "favorPoint": 0,
                    "potentialRank": 0,
                    "mainSkillLvl": 1,
                    "skin": charGet + "#1",
                    "level": 1,
                    "exp": 0,
                    "evolvePhase": 0,
                    "defaultSkillIndex": 0,
                    "gainTime": Ts,
                    "skills": []
                }
        """
        api.update(user, {
            'dexNav.character.' + newCharId: {
                'charInstId': newCharInstId,
                'count': 1
            },
            'building.chars.' + str(newCharInstId): {
                "charId": newCharId,
                "lastApAddTime": Ts,
                "ap": 8640000,
                "roomSlotId": "",
                "index": -1,
                "changeScale": 0,
                "bubble": {
                    "normal": {
                        "add": -1,
                        "ts": 0
                    },
                    "assist": {
                        "add": -1,
                        "ts": 0
                    }
                },
                "workTime": 0
            }
        })
        api.update(user, {'troop.chars.' + str(newCharInstId): newCharList[newChar]})
    return medium
