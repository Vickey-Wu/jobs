#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import csv
import telnetlib
import time
import threading


def IPspider(numpage):
    with open('ips.csv', 'w') as f:
        writer = csv.writer(f)
        url = 'http://www.xicidaili.com/nn/'
        user_agent = 'IP'
        headers = {'User-agent': user_agent}
        for num in range(1, numpage + 1):
            ipurl = url + str(num)
            response = requests.get(ipurl, headers=headers).text
            bs = BeautifulSoup(response, 'html.parser')
            res = bs.find_all('tr')
            for item in res:
                try:
                    temp = []
                    tds = item.find_all('td')
                    temp.append(tds[1].text)
                    temp.append(tds[2].text)
                    writer.writerow(temp)
                except IndexError:
                    pass


def get_proxy():
    proxy_l = []
    with open('ips.csv') as f:
        for i in f:
            row = i.strip().split(',')
            ip, port = row[0], row[1]
            proxy_l.append([ip, port])
    return proxy_l


def telnet_port(ip, port):
    try:
        tn = telnetlib.Telnet(ip, port, timeout=3)
        time.sleep(1)
        tn.close()
        with open('ip_available.csv', 'a') as f:
            f.write(ip + ' ' + port + '\n')
    except:
        pass
    time.sleep(1)


if __name__ == '__main__':
    # IPspider(2)
    # proxy_l = get_proxy()
    # mutex = threading.RLock()
    # task_l = []
    # for i in range(len(proxy_l)):
    #     task = threading.Thread(target=telnet_port, args=(proxy_l[i][0], proxy_l[i][1]))
    #     task_l.append(task)
    # for t in task_l:
    #     t.start()
    # for t1 in task_l:
    #     t1.join()
    ls = []
    # ls.append((city, str(companyId), companyLabel, companyName,  companyShortName, companySize,
    #                               education, financeStage, industryField, jobNature, leaderName, positionAdvantage,
    #                               positionFirstType, positionId, positionName, positionType, pvScore, workYear,
    #                               salaryMin, salaryMax, homeUrl, str(job_req)))
    print(type(("s")))



