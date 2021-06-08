#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Story System

from bottle import *
import json
from utils import api, logger, err

info_template = """
{
    "playerDataDelta": {
        "deleted": {},
        "modified": {}
    }
}
"""


@route('/story/finishStory', method='POST')
def story_finishStory():
    try:
        secret = request.get_header("secret")
        data = eval(request.body.read())
        storyId = data['storyId']
    except BaseException:
        return json.loads(err.badRequestFormat)

    if secret is None:
        return json.loads('{"result":1}')

    user = api.getUserBySecret(secret)

    if user is None:
        return json.loads('{"result":1}')

    filter = {'secret': secret}

    resp = """
{
    "playerDataDelta": {
        "modified": {
            "status": {
                "flags": {
                },
                "progress": 0
            }
        }
    }
}
    """
    medium = json.loads(resp)
    status = medium['playerDataDelta']['modified']['status']
    status['flags']['storyId'] = 1
    status['progress'] = user['status']['progress'] + 10

    api.update(user, {
        'status.flags.' + storyId: 1,
        'status.progress': user['status']['progress'] + 10
    })
    return
