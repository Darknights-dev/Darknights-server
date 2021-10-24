#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Account Register & User Init

from bottle import *
import json
import hashlib

from utils import logger, rnd, file, err, api


@route('/user/register', method='POST')
def user_register():
    """
    User register.
    """
    logger.info("Hit /user/register", request.environ.get('HTTP_X_FORWARDED_FOR'))

    try:
        data = eval(request.body.read())
    except BaseException:
        return json.loads(err.badRequestFormat)

    registerTs = int(time.time())

    account = data['account']
    passwd = data['password'] + 'kaltsit'
    passwd_hash = hashlib.md5(passwd.encode()).hexdigest()
    token = rnd.get_rand_str(32)

    logger.info("Read Initial User Data From Files")

    # Construct initial user data

    initial_chars = file.readFile('./serverData/userDataInit/troop_chars.json')
    initial_squads = file.readFile('./serverData/userDataInit/troop_squads.json')
    initial_charGroup = file.readFile('./serverData/userDataInit/troop_charGroup.json')
    initial_status = file.readFile('./serverData/userDataInit/status.json')
    initial_dexNav = file.readFile('./serverData/userDataInit/dexNav.json')
    initial_shop = file.readFile('./serverData/userDataInit/shop.json')
    initial_building = file.readFile('./serverData/userDataInit/building.json')
    initial_medal = file.readFile('./serverData/userDataInit/medal.json')
    initial_mission = file.readFile('./serverData/userDataInit/mission.json')
    initial_social = file.readFile('./serverData/userDataInit/social.json')
    initial_gacha = file.readFile('./serverData/userDataInit/gacha.json')

    """
    Stage & Retro List Generation Moved to sync
    """
    for index in initial_chars:
        initial_chars[index]['gainTime'] = registerTs

    # New User
    uid = api.getNewUid()
    initial_status['uid'] = uid
    userData = {
        "account": account,
        "uid": uid,
        "password": passwd_hash,
        "token": token,
        # Beginning of original user data
        "status": initial_status,
        "dungeon": {
            "stages": {},
            "cowLevel": {}
        },
        "troop": {
            "curCharInstId": len(initial_chars) + 1,
            "curSquadCount": 4,
            "squads": initial_squads,
            "chars": initial_chars,
            "charGroup": initial_charGroup,
            "charMission": {},
            "addon": {}
        },
        "dexNav": initial_dexNav,
        "building": initial_building,
        "medal": initial_medal,
        "mission": initial_mission,
        "gacha": initial_gacha,
        "skin": {
            "characterSkins": {},
            "skinTs": {}
        },
        "shop": initial_shop,
        "inventory": {},
        "social": initial_social,
        "storyreview": {
            "groups": {},
            "tags": {
                "knownStoryAcceleration": 0
            }
        },
        "retro": {
            'coin': 999,
            'supplement': 1,
            'block': {},
            'lst': -1,
            'nst': -1,
            'trial': {}
        },
        # End of original user data
        "battleReplay": {},
        "gachaStatus": {
            "guaranteed": 50,  # 保底数量(修改为0时无保底)
            "total": 0,  # 总抽取数量
            "save": 0  # 保底统计
        }
    }

    userData['status']['lastOnlineTs'] = registerTs
    userData['status']['lastRefreshTs'] = registerTs
    userData['status']['registerTs'] = registerTs

    inventoryList = file.readFile('./serverData/item_table.json')
    for i in inventoryList['items']:
        userData['inventory'][i] = 99999999

    api.addUser(userData)

    resp = """
{
    "expiresIn":604800,
    "isLatestUserAgreement":true,
    "issuedAt":0,
    "needAuthenticate":true,
    "result":0,
    "token":"",
    "uid":0
}
"""
    medium = json.loads(resp)
    medium['issuedAt'] = registerTs
    medium['token'] = token
    medium['uid'] = uid
    return medium


@route('/user/bindNickName', method='POST')
def user_bindNickName():
    """
    Change user name.
    """

    try:
        secret = request.get_header("secret")
        data = eval(request.body.read())
        nickName = data['nickName']
    except BaseException:
        return json.loads(err.badRequestFormat)

    if secret is None:
        return json.loads('{"result":1}')

    user = api.getUserBySecret(secret)

    if user is None:
        return json.loads('{"result":1}')

    user['status']['nickName'] = nickName
    user['status']['nickNumber'] = "001"

    api.update(user, {'status': user['status']})

    resp = """
{
    "playerDataDelta": {
        "deleted": {},
        "modified": {
            "status": {
                "nickName": "",
                "nickNumber": ""
            }
        }
    },
    "result": 0
}
"""
    medium = json.loads(resp)

    medium['playerDataDelta']['modified']['status']['nickName'] = nickName
    medium['playerDataDelta']['modified']['status']['nickNumber'] = "01"
    return medium


@route('/user/authenticateUserIdentity', method='POST')
@route('/user/checkIdCard', method='POST')
def user_checkIdCard():
    """
    F**king minor authentication
    """
    resp = """
{
    "isMinor": false,
    "message": "OK",
    "result": 0
}
                    """
    return json.loads(resp)


@route('/user/sendSmsCode', method='POST')
def user_sendSmsCode():
    """
    No, we have no intention to send smsCode.
    """
    return json.loads('{"result":0}')


@route('/protocol/service', method='GET')
def EULA():
    """
    Not handled yet.
    """
    HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1">
        <title>昨日方舟 - 使用许可及服务协议</title>
    </head>
    <body>
        <article>
        <h1>使用许可及服务协议</h1>
            <p>
                欢迎, darknights.
            </p>
        </article>
    </body>
</html>
    """
    return HTML
