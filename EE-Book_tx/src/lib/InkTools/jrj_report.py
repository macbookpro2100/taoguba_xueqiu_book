#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import time
import json
from src.tools.http import Http

import sys
from bs4 import BeautifulSoup

import urllib
# 修改默认编码
import sys

from src.tools.debug import Debug

reload(sys)

sys.setdefaultencoding('utf-8')

import random
import json
import time
import datetime

#  var%20BqswBhwL ???
# star_page = 1
# max_page = 7
# for raw_front_page_index in range(star_page, max_page):
#     time.sleep(1.0)
#     header = {'User-Agent': random.choice(my_headers)}
#     dfg = url.replace("{#}", u"".format(raw_front_page_index), 1)
#     dfg = dfg.replace("{=}", tagerCode, 1)
#     sdt = str((int(time.time() / 30)))
#     dfg = dfg.replace("{##}", sdt, 1)


from src.tools.path import Path

from multiprocessing import Pool


class JRJ_Report(object):
    def __init__(self):
        #   初始化目录结构

        return

    def start(self):
        print 'start JRJ_Report'

        stockList = []
        file_name = 'annual.txt'

        with open(file_name, 'r') as read_list:
            read_list = read_list.readlines()

            resultsL = read_list.__len__()
            for x in range(0, resultsL):
                line = read_list[x]
                splits = line.split('#')
                code = (str)(splits[0])
                fieName = (str)(splits[1]).strip()
                print fieName
                stockList.append({'URL': code, 'NAME': fieName})

        for xx in stockList:

            for raw_front_page_index in range(1, 8):

                fileN = str(xx['NAME']).strip()
                uux = xx['URL']

                sdPath = '/ink/work/62/ink/{}'.format(fileN)

                Path.mkdir(sdPath)

                url = u"http://istock.jrj.com.cn/yanbao_{}_p{}.html"

                request_url = url.format(uux, raw_front_page_index)
                content = Http.get_content(request_url)

                soup = BeautifulSoup(content, 'html.parser')

                list_p_list = soup.find_all('td', class_="left")

                for p in list_p_list:
                    # print p

                    list_pcyc_li = p.find_all('a')
                    for li in list_pcyc_li:
                        xxurl = li.get('href')
                        # print xxurl



                        if not 'http://istock.jrj.com.cn/list,yanbao.html' == xxurl :

                            time.sleep(1)
                            result = Http.get_content(xxurl)
                            result = unicode(str(result), 'GBK').encode('UTF-8')

                            xxsoup = BeautifulSoup(result, 'html.parser')

                            # title_tationl = xxsoup.find_all('h1')
                            # tt = str(title_tationl[0].text).strip()

                            xxlist_p_list = xxsoup.find_all('p', class_='title')[0]
                            xxlist_ds = xxsoup.find_all('span', class_='fr')[0]

                            realu = str(xxlist_p_list).replace(str(xxlist_ds), '', 1)

                            realuxsoup = BeautifulSoup(realu, 'html.parser')

                            sp = str(realuxsoup.text).split(' ')

                            ttime = sp[1]

                            if ttime.__contains__('发表于'):
                                ttime = sp[2]

                            # print (sp[2]).text
                            # print (sp[3]).text

                            # print ttime

                            all_main = xxsoup.find_all('div', class_='main')[0]

                            realuxsoup = BeautifulSoup(str(all_main), 'html.parser')

                            reaupp = realuxsoup.find_all('p')

                            for pp in reaupp:
                                list_pcyc_li = pp.find_all('a')

                                for li in list_pcyc_li:
                                    print li.text
                                    ttt = li.get('href')

                                    print ttt

                                    fileName = u"{}_{}.pdf".format(ttime, str(li.text).replace('/', ""))

                                    print fileName

                                    basePath = '/ink/work/62/ink/{}/{}'.format(fileN, fileName)

                                    Path.mkdirAndPath(basePath)

                                    Debug.print_in_single_line(u'开始下载   {}'.format(ttt))
                                    if ttt:
                                        content = Http.get_content(url=ttt, timeout=180)
                                        if not content:
                                            Debug.logger.debug(u'pdf『{}』下载失败'.format(ttt))
                                            content = ''
                                        else:
                                            Debug.print_in_single_line(u'pdf {} 下载完成'.format(ttt))
                                    else:
                                        #   当下载地址为空的时候，就没必要再去下载了
                                        content = ''
                                    if content.__len__() > 10:
                                        with open(basePath, "wb") as pdf:
                                            pdf.write(content)
