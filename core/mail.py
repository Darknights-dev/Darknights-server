#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Mail System

from bottle import *
import json
import time

from utils import logger


@route('/mail/getMetaInfoList', method='POST')
def mail_getMetaInfoList():
    logger.info('Hit /mail/getMetaInfoList', request.environ.get('HTTP_X_FORWARDED_FOR'))

    resp = """
{
    "playerDataDelta": {
        "deleted": {},
        "modified": {}
    },
    "result": [
        {
            "createAt": 1637998400,
            "hasItem": 1,
            "mailId": 1,
            "state": 0,
            "type": 1
        }
    ]
}
    """
    medium = json.loads(resp)
    medium['result'][0]['createAt'] = int(time.time())
    return medium


@route('/mail/listMailBox', method='POST')
def mail_listMailBox():
    logger.info('Hit /mail/listMailBox', request.environ.get('HTTP_X_FORWARDED_FOR'))

    resp = """
{
    "mailList": [
        {
            "content": "尊敬的博士：\\n感谢您一直以来对Darknights的理解与支持。\\n[Darknights]运营组",
            "createAt": 1625271400,
            "expireAt": 1919850600,
            "from": "penguin_logistics",
            "hasItem": 1,
            "items": [
                {
                    "count": 1,
                    "id": "renamingCard",
                    "type": "RENAMING_CARD"
                }
            ],
            "mailId": 1,
            "platform": -1,
            "state": 0,
            "style": {},
            "subject": "Welcome.",
            "type": 1,
            "uid": ""
        }
    ],
    "playerDataDelta": {
        "deleted": {},
        "modified": {}
    }
}
    """
    medium = json.loads(resp)
    return medium


@route('/mail/receiveAllMail', method='POST')
def mail_receiveAllMail():
    logger.info('Hit /mail/receiveAllMail', request.environ.get('HTTP_X_FORWARDED_FOR'))

    resp = """
{
    "items": [
        {
            "count": 1,
            "id": "renamingCard",
            "type": "RENAMING_CARD"
        }
    ],
    "playerDataDelta": {
        "deleted": {},
        "modified": {
            "consumable": {
                "renamingCard": {
                    "0": {
                        "count": 1,
                        "ts": -1
                    }
                }
            },
            "inventory": {
            },
            "pushFlags": {
                "hasGifts": 0
            },
            "status": {
            }
        }
    }
}
    """
    medium = json.loads(resp)
    return medium
