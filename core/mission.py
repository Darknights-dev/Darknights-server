#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Mission System

from bottle import *
import json

from utils import logger


@route('/mission/confirmMission', method='POST')
def mission_confirmMission():
    logger.info('Hit mission/confirmMission', request.environ.get('HTTP_X_FORWARDED_FOR'))

    data = json.loads(request.body.read())
    resp = """
{
    "items": [],
    "playerDataDelta": {
        "deleted": {},
        "modified": {
            "mission": {
                "missionRewards": {
                    "weeklyPoint": 1
                },
                "missions": {
                    "WEEKLY": {
                        "weekly_515": {
                            "state": 3
                        },
                        "weekly_516": {
                            "state": 2
                        }
                    }
                }
            }
        }
    }
}
    """
    medium = json.loads(resp)
    if str(data['missionId'])[0] == 'w':
        # weeklyPoint
        medium['playerDataDelta']['modified']['mission']['missionRewards'] = json.loads(
            '{"weeklyPoint": 1}')
    else:
        # dailyPoint
        medium['playerDataDelta']['modified']['mission']['missionRewards'] = json.loads(
            '{"dailyPoint": 1}')
    return medium


@route('/mission/exchangeMissionRewards', method='POST')
def mission_exchangeMissionRewards():
    logger.info("Hit mission/exchangeMissionRewards", request.environ.get('HTTP_X_FORWARDED_FOR'))

    data = json.loads(request.body.read())
    resp = """
{
    "items": [
        {
            "count": 1000,
            "id": "4001",
            "type": "GOLD"
        },
        {
            "count": 4,
            "id": "2001",
            "type": "CARD_EXP"
        }
    ],
    "playerDataDelta": {
        "deleted": {},
        "modified": {
            "inventory": {
                "2001": 320
            },
            "mission": {
                "missionRewards": {
                    "rewards": {
                        "WEEKLY": {
                            "reward_weekly_101": 1
                        }
                    },
                    "weeklyPoint": 0
                }
            },
            "status": {
                "gold": 153333
            }
        }
    }
}
    """
    medium = json.loads(resp)
    if str(data['targetRewardsId'])[7] == 'w':
        # weekly
        medium['playerDataDelta']['modified']['mission']['missionRewards']['rewards']['WEEKLY'] = json.loads(
            '{"' + str(data['targetRewardsId']) + '":1}')
    else:
        # daily
        medium['playerDataDelta']['modified']['mission']['missionRewards']['rewards'] = json.loads(
            '{"DAILY":{"' + str(data['targetRewardsId']) + '":1}}')

    return medium
