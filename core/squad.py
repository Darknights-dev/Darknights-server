#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Squad System

from bottle import *
import json

from utils import logger, api, err


@route('/quest/squadFormation', method='POST')
def quest_squadFormation():
    """
    Save squad data to db and response new squad.
    """
    logger.info('Hit /quest/squadFormation', request.environ.get('HTTP_X_FORWARDED_FOR'))

    try:
        secret = request.get_header("secret")
        data = json.loads(request.body.read())
        squadId = data['squadId']
        slots = data['slots']
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
                "squads": {
                }
            }
        }
    }
}
"""
    medium = json.loads(resp)
    medium['playerDataDelta']['modified']['troop']['squads'][str(squadId)] = {'slots': slots}

    api.update(user, {'troop.squads.' + str(squadId) + '.slots': slots})

    return medium


@route('/quest/changeSquadName', method='POST')
def quest_changeSquadName():
    """
    Save squad name to db and response new squad name.
    """
    logger.info('Hit /quest/changeSquadName', request.environ.get('HTTP_X_FORWARDED_FOR'))
    try:
        secret = request.get_header("secret")
        data = json.loads(request.body.read())
        squadId = data['squadId']
        name = data['name']
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
                "squads": {
                }
            }
        }
    },
    "result": 0
}
    """
    medium = json.loads(resp)
    medium['playerDataDelta']['modified']['troop']['squads'][str(squadId)] = {'name':name}

    api.update(user, {'troop.squads.' + str(squadId) + '.name': name})
    return medium
