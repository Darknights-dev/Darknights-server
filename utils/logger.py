#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Logging System

import time
import sys
import os


def info(inform, client_ip='localhost'):
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    dt = time.strftime("%Y-%m-%d", time.localtime())
    msg = f'[{ts}][{client_ip}][INFO] {inform}'
    print(msg)
    log_file = open(f'./logs/log-{dt}.log', 'a', encoding='utf-8')
    log_file.write(msg + '\n')
    log_file.close()


def warn(warning, client_ip='localhost'):
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    dt = time.strftime("%Y-%m-%d", time.localtime())
    msg = f'[{ts}][{client_ip}][INFO] {warning}'
    print('#'*10)
    print(msg)
    print('#'*10)
    log_file = open(f'./logs/log-{dt}.log', 'a', encoding='utf-8')
    log_file.write('#'*10)
    log_file.write(msg + '\n')
    log_file.write('#'*10)
    log_file.close()
