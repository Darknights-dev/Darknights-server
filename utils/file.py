#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: File Operation Class

import json


def readFile(fileName, evals=True):
    with open(fileName, 'r', encoding='utf-8') as f:
        if evals:
            return json.loads(f.read())
        return f.read()
