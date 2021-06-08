#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Random Class

import random
import string


def get_rand_str(n):
    str_list = [
        random.choice(
            string.digits +
            string.ascii_letters) for i in range(n)]
    random_str = ''.join(str_list)
    return random_str
