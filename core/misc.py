#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Something else

from bottle import *
import json

from utils import api, err, logger


@route('/user/changeSecretary', method='POST')
def user_changeSecretary():
    return None


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
                "diamondShard": 0
            }
        }
    }
}
    """
    medium = json.loads(resp)
    modify = medium['playerDataDelta']['modified']
    modify['status']['androidDiamond'] = user['status']['androidDiamond'] - count
    modify['status']['diamondShard'] = user['status']['diamondShard'] + 180 * count

    api.update(user, {
        'status.androidDiamond': user['status']['androidDiamond'] - count,
        'status.diamondShard': user['status']['diamondShard'] + 180 * count
    })
    return medium
