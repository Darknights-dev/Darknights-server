#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Something else

from bottle import *
import json

from utils import api, err, logger


@route('/background/setBackground', method='POST')
def setBackground():
    logger.info('/background/setBackground', request.environ.get('HTTP_X_FORWARDED_FOR'))
    try:
        secret = request.get_header("secret")
        data = json.loads(request.body.read())
        bgID = data['bgID']
    except BaseException:
        return json.loads(err.badRequestFormat)

    if secret is None:
        return json.loads('{"result":1}')

    user = api.getUserBySecret(secret)

    api.update(user, {'background.selected': bgID})

    resp = """
{
    "playerDataDelta": {
        "deleted": {},
        "modified": {
            "background": {
                "selected": "bg_rhodes_day"
            }
        }
    }
}
"""
    medium = json.loads(resp)
    medium["playerDataDelta"]["modified"]["background"]["selected"] = bgID

    return medium


@route('/user/changeSecretary', method='POST')
def user_changeSecretary():
    logger.info('/user/changeSecretary', request.environ.get('HTTP_X_FORWARDED_FOR'))
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

    charId = api.getCharIdByCharInstId(user, charInstId)

    resp = """
{
    "playerDataDelta": {
        "deleted": {},
        "modified": {
            "status": {
                "avatar": {
                    "id": "char_010_chen#2",
                    "type": "ASSISTANT"
                },
                "secretary": "char_010_chen",
                "secretarySkinId": "char_010_chen#2"
            }
        }
    }
}
    """
    medium = json.loads(resp)
    modify = medium['playerDataDelta']['modified']
    modify['status']['avatar'] = {'id': charId, 'type': 'ASSISTANT'}
    modify['status']['secretary'] = charId
    modify['status']['secretarySkinId'] = skinId
    api.update(user, {'status.secretary': charId})
    api.update(user, {'status.secretarySkinId': skinId})
    return medium


@route('/user/updateAgreement', method='POST')
def update_Agreement():
    resp = """
{
    "orderIdList": [],
    "playerDataDelta": {
        "deleted": {},
        "modified": {}
        }
}
    """
    return json.loads(resp)


@route('/user/exchangeDiamondShard', method='POST')
def user_exchangeDiamondShard():
    """
    Change user diamond to diamondShard.
    """
    logger.info('Hit /gacha/exchangeDiamondShard', request.environ.get('HTTP_X_FORWARDED_FOR'))

    try:
        secret = request.get_header("secret")
        data = json.loads(request.body.read())
        count = data['count']
    except BaseException:
        return json.loads(err.badRequestFormat)

    if secret is None:
        return json.loads('{"result":1}')

    user = api.getUserBySecret(secret)

    if user is None:
        return json.loads('{"result":1}')

    if count > user['status']['androidDiamond']:
        return json.loads('{"result":1}')

    resp = """
{
    "playerDataDelta": {
        "deleted": {},
        "modified": {
            "status": {
                "androidDiamond": 0,
                "iosDiamond": 0,
                "diamondShard": 0
            }
        }
    }
}
    """
    medium = json.loads(resp)
    modify = medium['playerDataDelta']['modified']
    modify['status']['iosDiamond'] = modify['status']['androidDiamond'] = user['status']['androidDiamond'] - count
    modify['status']['diamondShard'] = user['status']['diamondShard'] + 180 * count

    api.update(user, {
        'status.androidDiamond': modify['status']['androidDiamond'],
        'status.iosDiamond': modify['status']['androidDiamond'],
        'status.diamondShard': modify['status']['diamondShard']
    })
    return medium
