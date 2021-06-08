#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: Core EntryPoint

import os
path = os.getcwd() + '/core/'
files = os.listdir(path)
__all__ = []
for i in files:
    __all__.append(i.replace('.py', ''))
