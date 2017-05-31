#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Usage: spider_jianshu.py -k <keyword> [-t <num>]
-t                 thread num [default:2]
-v --version       show version
-h --help          show this help
"""
import Queue
import json
import random
import re
import threading
from collections import deque
import requests
from docopt import docopt


que = Queue.Queue()


def get_user_agent():
    platform = random.choice(['Macintosh', 'Windows', 'X11'])
    if platform == 'Macintosh':
        os = random.choice(['68K', 'PPC'])
    elif platform == 'Windows':
        os = random.choice(['Win3.11', 'WinNT3.51', 'WinNT4.0',
                            'Windows NT 5.0', 'Windows NT 5.1',
                            'Windows NT 5.2', 'Windows NT 6.0',
                            'Windows NT 6.1', 'Windows NT 6.2',
                            'Win95', 'Win98', 'Win 9x 4.90', 'WindowsCE'])
    elif platform == 'X11':
        os = random.choice(['Linux i686', 'Linux x86_64'])

    browser = random.choice(['chrome', 'firefox', 'ie'])
    if browser == 'chrome':
        webkit = str(random.randint(500, 599))
        version = str(random.randint(0, 24)) + '.0' + \
                  str(random.randint(0, 1500)) + '.' + \
                  str(random.randint(0, 999))
        return 'Mozilla/5.0 (' + os + ') AppleWebKit/' + webkit + \
               '.0 (KHTML, live Gecko) Chrome/' + version + ' Safari/' + webkit
    elif browser == 'firefox':
        year = str(random.randint(2000, 2012))
        month = random.randint(1, 12)
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)
        day = random.randint(1, 30)
        if day < 10:
            day = '0' + str(day)
        else:
            day = str(day)
        gecko = year + month + day
        version = random.choice(map(lambda x: str(x) + '.0', range(1, 16)))
        return 'Mozilla/5.0 (' + os + '; rv:' + version + ') Gecko/' + \
               gecko + ' Firefox/' + version
    elif browser == 'ie':
        version = str(random.randint(1, 10)) + '.0'
        engine = str(random.randint(1, 5)) + '.0'
        option = random.choice([True, False])
        if option:
            token = random.choice(['.NET CLR', 'SV1', 'Tablet PC', 'WOW64',
                                   'Win64; IA64', 'Win64; x64']) + '; '
        elif option is False:
            token = ''
        return 'Mozilla/5.0 (compatible; MSIE ' + version + '; ' + os + \
               '; ' + token + 'Trident/' + engine + ')'


def get_headers():

    headers = {
        "Host": "www.jianshu.com",
        "Connection": "keep-alive",
        "Accept": "application/json",
        "User-Agent": get_user_agent(),
        "Referer": "http://www.jianshu.com/search?q=python&page="+str(random.randint(1,10))+"&type=note",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8"
    }
    return headers


def get_total_pages(keyword):
    url = 'http://www.jianshu.com/search/do?q='+keyword+'&type=note&page=0&order_by=default'
    r = requests.get(url,headers=get_headers(),timeout=20)
    return r.json()['total_pages']


class Spider(object):
    def __init__(self,keyword):
        self.keyword = str(keyword)
        self.d = deque(xrange(get_total_pages(self.keyword)))

    def _url_constructor(self,slug):
        return 'http://www.jianshu.com/p/'+str(slug)

    def get_pdata(self,pagenum):
        url = 'http://www.jianshu.com/search/do?q='+self.keyword+'&type=note&page='+str(pagenum)+'&order_by=default'
        print url
        r = requests.get(url,headers=get_headers(),timeout=20)
        for i in r.json()['entries']:
            #print i['id'],i['slug'],re.sub(r"<.*?>",'',i['title'])
            que.put({i['id']:[re.sub(r"<.*?>",'',i['title']),self._url_constructor(i['slug'])]})
        que.put('over')

    def go(self):
        while len(self.d) > 0:
            self.get_pdata(self.d.popleft()+1)

    def get_que_data(self):
        tmpl=[]
        while True:
            if not que.empty():
                q = que.get()
                if q == 'over':
                    tmpl.append(q)
                else:
                    print json.dumps(q, encoding='UTF-8', ensure_ascii=False)
                if tmpl.__len__() == 10:
                    break

    def run(self):
        tlist=[]
        funclist = [self.go for _ in range(3)]
        funclist.append(self.get_que_data)
        for f in funclist:
            t = threading.Thread(target=f)
            t.start()
            tlist.append(t)
        for t in tlist:
            t.join()


def main():
    # arguments = docopt(__doc__, version='spider 1.0')
    arguments = {}
    arguments['<keyword>'] = 'iOS'
    sp = Spider(arguments['<keyword>'])
    sp.run()


if __name__ == '__main__':
    main()