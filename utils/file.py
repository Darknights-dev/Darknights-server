#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: File Operation Class

import json

null = 'null'
true = True
false = False


def readFile(fileName, intercept=True):
    with open(fileName, 'r', encoding='utf-8') as f:
        if intercept:
            return json.loads(f.read())
        return f.read()
