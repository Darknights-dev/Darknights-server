#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Infrastructure System

from bottle import *
import json


@route('/building/settleManufacture', method='POST')
@route('/building/gainAllIntimacy', method='POST')
@route('/building/buyLabor', method='POST')
@route('/building/deliveryBatchOrder', method='POST')
@route('/building/getMeetingroomReward', method='POST')
@route('/building/getInfoShareVisitorsNum', method='POST')
def getInfoShareVisitorsNum():
    return json.loads('{"num":0}')


@route('/building/getRecentVisitors', method='POST')
def getRecentVisitors():
    return json.loads('{"visitors":[]}')
