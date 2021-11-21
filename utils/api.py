#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Api

# Database operation
import pymongo
import copy
import time

from utils import logger, file

main_client = pymongo.MongoClient("mongodb://localhost:27017/", connect=False)
logger.info('Connecting to database.')
main_db = main_client["Darknights"]
user_rol = main_db['users']

# init DB
status = user_rol.find_one({'system': 1})
if not status:
    user_rol.insert_one({'system': 1, 'user_count': 0})


def getUserCount():
    dbStatus = user_rol.find_one({'system': 1})
    userCount = dbStatus['user_count']
    return userCount


def getNewUid():
    uid = getUserCount() + 1
    user_rol.update_one({'system': 1}, {'$set': {'user_count': uid}})
    return uid


def addUser(data):
    user_rol.insert_one(data)
    return


def getUserByAccount(account):
    user = user_rol.find_one({'account': account})
    return user


def getUserByToken(token):
    user = user_rol.find_one({'token': token})
    return user


def getUserByToken24(token):
    user = user_rol.find_one({'token_24': token})
    return user


def getUserBySecret(secret):
    user = user_rol.find_one({'secret': secret})
    return user


def getTs():
    return int(time.time())


def completeServerData(user, Ts):
    """
    Completion of New Data
    If serverData changes, this function will auto complete missing stages, retros, backgrounds, etc.
    """
    stageTable = file.readFile('./serverData/stage_table.json')
    retroTable = file.readFile('./serverData/retro_table.json')
    displayTable = file.readFile('./serverData/display_meta_table.json')
    itemTable = file.readFile('./serverData/item_table.json')

    # Construct stages

    emptyStage = {
        "stageId": "",
        "completeTimes": 0,
        "startTimes": 0,
        "practiceTimes": 0,
        "state": 2,
        "hasBattleReplay": 0,
        "noCostCnt": 0
    }

    for name in stageTable['stages'].keys():
        if name not in user['dungeon']['stages']:
            emptyStage['stageId'] = name
            if name.startswith('guide'):
                emptyStage['state'] = 3
            else:
                emptyStage['state'] = 2
            user['dungeon']['stages'][str(name)] = copy.deepcopy(emptyStage)

    # Construct retro
    locked = {
        "locked": 1,
        "open": 1
    }
    for name in retroTable['zoneToRetro'].values():
        if name not in user['retro']['block']:
            user['retro']['block'][name] = locked

    # Background
    for name in displayTable['homeBackgroundData']['homeBgDataList']:
        if name['bgId'] not in user['background']['bgs']:
            user['background']['bgs'][name['bgId']] = {'unlock': Ts}

    # Item
    for name in itemTable['items']:
        if name not in user['inventory']:
            user['inventory'][name] = 99999

    return user


def loadUserData(user, template):
    template['user']['status'] = user['status']
    # No difference between android and ios
    template['user']['status']['iosDiamond'] = template['user']['status']['androidDiamond']
    template['user']['dungeon'] = user['dungeon']  # Semi-Unlocked
    template['user']['troop'] = user['troop']
    template['user']['dexNav']['character'] = user['dexNav']['character']
    template['user']['building'] = user['building']
    template['user']['inventory'] = user['inventory']
    template['user']['storyreview'] = user['storyreview']
    template['user']['retro'] = user['retro']
    template['user']['background']['selected'] = user['background']['selected']
    return template


def updateAllTs(user, medium, Ts):
    # Update all timestamps
    medium['user']['pushFlags']['status'] = Ts
    medium['user']['status']['lastOnlineTs'] = Ts
    medium['user']['status']['lastRefreshTs'] = Ts
    medium['user']['campaignsV2']['lastRefreshTs'] = Ts
    medium['user']['event']['building'] = Ts
    medium['ts'] = Ts
    return medium


def updateUserData(user, template):
    update(user, {'status': template['user']['status']})
    update(user, {'retro': template['user']['retro']})
    update(user, {'pushFlags': template['user']['pushFlags']})
    update(user, {'dungeon.stages': template['user']['dungeon']['stages']})
    update(user, {'inventory': template['user']['inventory']})


def update(user, data):
    uid = user['uid']
    user_rol.update_one({'uid': uid}, {"$set": data})
    return


def addItem(user, items):
    uid = user['uid']
    for i in items:
        if user['inventory'][i]:
            update(user, {'inventory.' + i: user['inventory'][i] + 1})
        else:
            update(user, {'inventory.' + i: 1})
    return


def getCharIdByCharInstId(user, charInstId):
    return user['troop']['chars'][str(charInstId)]['charId']


def getCharInstIdByCharId(user, charId):
    return user['dexNav']['character'][str(charId)]['charInstId']
