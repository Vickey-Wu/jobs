#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @date: 2018/2/23 22:16 
# @name: tmp
# @author：vickey-wu

from urllib import request
from bs4 import BeautifulSoup

resp = request.urlopen("https://www.zhipin.com/job_detail/1417782228.html").read().decode("utf-8")
soup = BeautifulSoup(resp,'lxml')
requirement = soup.find_all(class_="text")[0]
print(type(str(requirement)), requirement)