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

# 常量部分
oneAdvancedGachaCost = 600  # 合成玉消耗
percentageSSSR = 2  # 六星概率
percentageSSSRAdd = 2  # 保底概率增加
percentageSSR = 8  # 五星概率
percentageSR = 50  # 四星概率
chanceUp = [[], [], [], []]  # 特殊UP活动,分别对应3、4、5、6
selfDefined = False  # 是否自定义抽卡,该项为True时不进行随机生成.
selfDefinedList = []  # 自定义抽卡数据，填入干员ID，不知道的可访问/showDb查看。一定要填满十个！

# 统计用变量
listR = [[], [], [], []]  # 干员列表
listName = [[], [], [], []]  # 干员名
fullCharList = {}  # 全部干员信息
listCount = [0, 0, 0, 0, 0, 0]  # 抽取数量统计

# 公招限定
charNotIncluded = {'estell', 'savage', 'grani', 'tiger', 'hpsts', 'amiya'}


def charListInit():
    global listR, listCount, fullCharList
    charCount = 0
    with open('./serverData/character_table.json', 'r', encoding='utf-8') as infile:
        js = json.loads(infile.read())
        for (key, value) in js.items():
            if value["isNotObtainable"]:
                continue
            if not key.startswith('char'):
                continue
            for limit in charNotIncluded:
                if key.endswith(limit):
                    continue
            rarity = value["rarity"]
            fullCharList[key] = value
            listR[rarity - 2].append(key)
            listName[rarity - 2].append(value['name'])
            listCount[rarity - 2] += 1
            charCount += 1
    logger.info(str(charCount) + ' Gacha-able Operators Loaded.')


charListInit()


@route('/chars')
def print_db():
    output = '''<!DOCTYPE html>
    <html>
    <head> 
    <meta charset="utf-8" /> 
    <title>干员列表</title> 
    </head> 
    <body> 

    '''
    rare_list = ['三星', '四星', '五星', '六星']
    for i in range(4):
        output += ('<center style="font-size:18px;color:#FF0000">' + rare_list[i] + '</center>\n<center>')
        for j in range(len(listR[i])):
            output += (listName[i][j] + ' : ' + listR[i][j] + '<br/>')
        output += '</center>'
    output += '''
    </body>
    </html>
    '''
    return output


def getChance(user):
    startAdd = user['gachaStatus']['guaranteed']
    save = user['gachaStatus']['save']

    sssr_percentage = percentageSSSR
    if startAdd == 0:
        return sssr_percentage
    if save > startAdd:
        sssr_percentage += (save - startAdd) * percentageSSSRAdd
    return sssr_percentage


def getGachaItem(rarity):
    l1 = len(listR[rarity - 3])
    l2 = len(chanceUp[rarity - 3])
    if l2 != 0:
        if random.randrange(1, 3) == 1:
            return chanceUp[rarity - 3][random.randrange(0, l2)]
    return str(listR[rarity - 3][random.randrange(0, l1)])


def gachaGetOne(user):
    total = user['gachaStatus']['total']
    save = user['gachaStatus']['save']
    num = random.randrange(1, 101)
    chance = getChance(user)

    if num <= chance:
        # SSSR
        total += 1
        save = 0
        api.update(user, {'gachaStatus.save': save})
        api.update(user, {'gachaStatus.total': total})
        return getGachaItem(6)
    elif num <= chance + percentageSSR:
        # SSR
        total += 1
        save += 1
        api.update(user, {'gachaStatus.save': save})
        api.update(user, {'gachaStatus.total': total})
        return getGachaItem(5)
    elif num <= chance + percentageSSR + percentageSR:
        # SR
        total += 1
        save += 1
        api.update(user, {'gachaStatus.save': save})
        api.update(user, {'gachaStatus.total': total})
        return getGachaItem(4)
    else:
        # R
        total += 1
        save += 1
        api.update(user, {'gachaStatus.save': save})
        api.update(user, {'gachaStatus.total': total})
        return getGachaItem(3)


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

    if diamondShard - oneAdvancedGachaCost < 0:
        return json.loads('{"result":1}')

    """
    charInstId saved in user['troop']['chars']
    charName saved in user['dexNav']['character']
    Do not forget to modify building.
    """
    Ts = int(time.time())

    curCharInstId = user['troop']['curCharInstId']
    charGet = gachaGetOne(user)
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
        'id': "p_" + charGet,  # May cause bugs in the future
        'type': 'MATERIAL'
    })

    modify = medium['playerDataDelta']['modified']

    modify['inventory']['p_' + charGet] = 1

    modify['status']['diamondShard'] = diamondShard - oneAdvancedGachaCost
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
        'status.diamondShard': diamondShard - oneAdvancedGachaCost
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

    if user['status']['diamondShard'] - 10 * oneAdvancedGachaCost < 0:
        return json.loads('{"result":1}')

    Ts = int(time.time())

    gachaResultList = []  # gacha result, all chars directly send back
    instIdResult = {}  # save generated char's instId
    newCharList = {}  # real NEW char (not obtain yet)
    inventory = {}  # char's inventory

    curCharInstId = user['troop']['curCharInstId']

    for num in range(10):
        charGet = gachaGetOne(user)

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
    modify['status']['diamondShard'] = user['status']['diamondShard'] - 10 * oneAdvancedGachaCost
    modify['status']['lggShard'] = user['status']['lggShard'] + 10 * 10
    api.update(user, {
        'status.lggShard': user['status']['lggShard'] + 10 * 10,
        'status.diamondShard': user['status']['diamondShard'] - 10 * oneAdvancedGachaCost,
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
