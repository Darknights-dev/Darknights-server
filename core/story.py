#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Story System

from bottle import *
import json
from utils import api, logger, err


@route('/story/finishStory', method='POST')
def story_finishStory():
    logger.info("Hit /story/finishStory", request.environ.get('HTTP_X_FORWARDED_FOR'))

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
    status['flags'][storyId] = 1
    status['progress'] = user['status']['progress'] + 10

    api.update(user, {
        'status.flags.' + storyId: 1,
        'status.progress': user['status']['progress'] + 10
    })
    return medium


@route('/quest/finishStoryStage', method='POST')
def quest_finishStoryStage():
    """
    Can not enter story view
    """
    resp = """
{
    "alert": [],
    "playerDataDelta": {
        "deleted": {},
        "modified": {
        }
    },
    "result": 0,
    "rewards": [],
    "unlockStages": []
}
"""
    return json.loads(resp)


@route('/storyreview/markStoryAcceKnown', method='POST')
def storyreview_markStoryAcceKnown():
    logger.info('Hit /storyreview/markStoryAcceKnown', request.environ.get('HTTP_X_FORWARDED_FOR'))

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
        "orderIdList": [],
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "storyreview":{
                    "tags":{
                        "knownStoryAcceleration": 1
                        }
                    }
                }
            }
    }
        """
    api.update(user, {
        'storyreview.tags.knownStoryAcceleration': 1
    })
    return json.loads(resp)
