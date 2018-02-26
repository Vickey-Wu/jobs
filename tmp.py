#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @date: 2018/2/23 22:16 
# @name: tmp
# @author：vickey-wu

import math

for i in range(10000):
    if i % 11 == 7 and i % 7 == 5 and i % 5 == 3 and i % 3 == 2:
        print(i)