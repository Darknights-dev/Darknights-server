#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Encryption Unit

import time
import json
import string
import random
import hashlib

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

LOG_TOKEN_KEY = "pM6Umv*^hVQuB6t&{login_time}"


def get_rand_str(n):
    str_list = [
        random.choice(string.digits + string.ascii_letters) for i in range(n)]
    random_str = ''.join(str_list)
    return random_str


def get_md5(src):
    return hashlib.md5(src.encode()).hexdigest()


def rijndael_decrypt(data, key, iv):
    aes_obj = AES.new(key, AES.MODE_CBC, iv)
    decrypt_buf = aes_obj.decrypt(data)
    return unpad(decrypt_buf, AES.block_size)


def decrypt_battle_data(data, login_time):
    battle_data = data[:-32:]
    battle_data_array = bytearray.fromhex(battle_data)
    iv = data[-32::]
    iv_array = bytearray.fromhex(iv)
    key_array = bytearray.fromhex(get_md5(LOG_TOKEN_KEY.format(login_time=login_time)))
    return rijndael_decrypt(battle_data_array, key_array, iv_array).decode()
