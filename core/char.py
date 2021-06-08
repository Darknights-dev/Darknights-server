#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Char Build System

from bottle import *
import json, time

from utils import logger, api, err

with open('./serverData/gamedata_const.json', 'r', encoding='utf-8') as f:
    constConfig = json.loads(f.read())
    logger.info('Constant Gamedata Loaded.')


@route('/charBuild/boostPotential', method='POST')
def charBuild_boostPotential():
    logger.info('Hit /charBuild/boostPotential', request.environ.get('HTTP_X_FORWARDED_FOR'))

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
    logger.info('Hit /charBuild/upgradeChar', request.environ.get('HTTP_X_FORWARDED_FOR'))

    try:
        secret = request.get_header("secret")
    except BaseException:
        return json.loads(err.badRequestFormat)

    if secret is None:
        return json.loads('{"result":1}')
    user = api.getUserBySecret(secret)

    if user is None:
        return json.loads('{"result":1}')
    return


@route('/charBuild/changeCharSkin', method='POST')
def charBuild_changeCharSkin():
    logger.info('Hit /charBuild/changeCharSkin', request.environ.get('HTTP_X_FORWARDED_FOR'))

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
    medium['playerDataDelta']['modified']['troop']['chars'][str(charInstId)] = {"skin": skinId}
    return medium


@route('/charBuild/evolveChar', method='POST')
def charBuild_evolveChar():
    return
