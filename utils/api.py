#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Api

# Database operation
import pymongo

from utils import logger

main_client = pymongo.MongoClient("mongodb://localhost:27017/", connect=False)
logger.info('Connecting to database.')
main_db = main_client["Darknights"]
user_rol = main_db['users']

# init DB
status = user_rol.find_one({'system': 1})
if not status:
    user_rol.insert_one({'system': 1, 'user_count': 0})


def getUserCount():
    dbStatus = user_rol.find_one({'system': 1})
    userCount = dbStatus['user_count']
    return userCount


def getNewUid():
    uid = getUserCount() + 1
    user_rol.update_one({'system': 1}, {'$set': {'user_count': uid}})
    return uid


def addUser(data):
    user_rol.insert_one(data)
    return


def getUserByAccount(account):
    user = user_rol.find_one({'account': account})
    return user


def getUserByToken(token):
    user = user_rol.find_one({'token': token})
    return user


def getUserByToken24(token):
    user = user_rol.find_one({'token_24': token})
    return user


def getUserBySecret(secret):
    user = user_rol.find_one({'secret': secret})
    return user


def update(user, data):
    uid = user['uid']
    user_rol.update_one({'uid': uid}, {"$set": data})
    return


def addItem(user, items):
    uid = user['uid']
    for i in items:
        if user['inventory'][i]:
            update(user, {'inventory.' + i: user['inventory'][i] + 1})
        else:
            update(user, {'inventory.' + i: 1})
    return
