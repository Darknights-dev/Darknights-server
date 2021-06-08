#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Logging System

import time
import sys
import os


def info(info, client_ip='localhost'):
    msg = '[' + str(time.strftime("%Y-%m-%d %H:%M:%S",
                                  time.localtime())) + '][' + str(client_ip) + '][INFO] ' + info
    print(msg)
    log_file = open(
        './logs/log-' +
        time.strftime(
            "%Y-%m-%d",
            time.localtime()) +
        '.log',
        'a',
        encoding='utf-8')
    log_file.write(msg + '\n')
    log_file.close()
