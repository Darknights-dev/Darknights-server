#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Checkin System

from bottle import *
import json

from utils import logger, api, err

with open('./serverData/checkin_table.json', 'r', encoding='utf-8') as f:
    logger.info('CheckIn Data Loaded.')
    checkIn_table = eval(f.read())


@route('/user/checkIn', method='POST')
def user_checkin():
    logger.info('Hit /user/checkIn', request.environ.get('HTTP_X_FORWARDED_FOR'))

    try:
        secret = request.get_header("secret")
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
            "checkIn": {
                "canCheckIn": 0,
                "checkInHistory": [
                    0
                ]
            },
            "status": {
            }
        }
    },
    "signInRewards": [
        {
            "count": 2000,
            "id": "4001",
            "type": "GOLD"
        }
    ],
    "subscriptionRewards": []
}
    """
    medium = json.loads(resp)
    return medium
