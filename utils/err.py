#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Definition of errors

import json

badRequestFormat = {
    "error": "Bad Request",
    "message": "Invalid request payload JSON format",
    "statusCode": 400
}

status1 = json.loads("""{"result": 1}""")
