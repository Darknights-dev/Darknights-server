#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Retro-Story System

from bottle import *
import json

from utils import logger, file, err, api


@route('/retro/unlockRetroBlock', method='POST')
def retro_unlockRetroBlock():
    """
    Unlock Retro Story
    """
    logger.info("Hit /retro/unlockRetroBlock", request.environ.get('HTTP_X_FORWARDED_FOR'))

    try:
        secret = request.get_header("secret")
        data = json.loads(request.body.read())
        retroId = data['retroId']
    except BaseException:
        return json.loads(err.badRequestFormat)

    if secret is None:
        return json.loads('{"result":1}')

    user = api.getUserBySecret(secret)

    if user is None:
        return json.loads('{"result":1}')

    unlock = {
        "locked": 0,
        "open": 1
    }
    coin = user['retro']['coin'] - 1
    resp = """
{
    "playerDataDelta": {
        "deleted": {},
        "modified": {
            "retro": {
                "block": {},
                "coin": 2
            }
        }
    }
}
    """
    medium = json.loads(resp)
    modify = medium['playerDataDelta']['modified']
    modify['retro']['coin'] = coin
    modify['retro']['block'][retroId] = unlock

    api.update(user, {'retro.coin': coin})
    api.update(user, {'retro.block.' + retroId: unlock})
    return medium
