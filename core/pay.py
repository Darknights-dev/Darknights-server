#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Payment

"""
No, we will not do any payment.
"""
from bottle import *
import json
from utils import logger


@route('/pay/getUnconfirmedOrderIdList', method='POST')
def pay_getUnconfirmedOrderIdList():
    logger.info('Hit /pay/getUnconfirmedOrderIdList', request.environ.get('HTTP_X_FORWARDED_FOR'))

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


@route('/pay/createOrder', method='POST')
def pay_createOrder():
    logger.info('Hit /pay/createOrder', request.environ.get('HTTP_X_FORWARDED_FOR'))
    resp = """
{
    "alertMinor": 0,
    "extension": "",
    "orderId": "20770230191981000063369555114514",
    "playerDataDelta": {
        "deleted": {},
        "modified": {}
    },
    "result": 0
}
    """
    return json.loads(resp)


@route('/u8/pay/confirmOrderState', method='POST')
def u8_pay_confirmOrderState():
    resp = """
{
    "payState": 3
}
    """
    return json.loads(resp)


@route('/pay/confirmOrderAlipay', method='POST')
def pay_confirmOrderAlipay():
    resp = """
{
    "status": 0
}
    """
    return json.loads(resp)


@route('/pay/confirmOrder', method='POST')
def pay_confirmOrder():
    resp = """
{
    "goodId": "GP_Once_1",
    "playerDataDelta": {
        "deleted": {},
        "modified": {
            "status": {
            }
        }
    },
    "receiveItems": {
        "items": []
    },
    "result": 0
}
    """
    return json.loads(resp)
