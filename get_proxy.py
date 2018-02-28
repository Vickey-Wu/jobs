#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from urllib import request
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
            ip_url = url + str(num)
            response = requests.get(ip_url, headers=headers).text
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


def get_ip_and_port():
    ip_port = []
    with open('ips.csv') as f:
    # with open('ip_available.csv') as f:
        for i in f:
            row = i.strip().split(':')
            # row = i.strip().split(' ')
            ip, port = row[0], row[1].strip()
            ip_port.append([ip, port])
    return ip_port

def verification(ip, port):
    # for n in range(len(ip_port)):
        req = request.Request("https://www.baidu.com")
        # req = request.Request("https://www.google.com")
        req.set_proxy(host=ip + ":" + port, type="https")
        try:

            response = request.urlopen(req, timeout=10)
        except Exception as e:
            # print("request error", e, ip)
            # continue
            pass
        else:
            status = response.getcode()
            if status >= 200 and status < 300:
                print( ip + ": " + port)
            else:
                # print("invalid proxy:", status)
                pass
        time.sleep(1)
        # thread_max.release()


# verification()

if __name__ == '__main__':
    # IPspider(10)
    # thread_max = threading.BoundedSemaphore(100)
    ip_port = get_ip_and_port()
    mutex = threading.RLock()
    task_l = []
    for i in range(6):
        # thread_max.acquire()
        task = threading.Thread(target=verification, args=(ip_port[i][0], ip_port[i][1]))
        task_l.append(task)
    for t in task_l:
        t.start()
    for t1 in task_l:
        t1.join()
