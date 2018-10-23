#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import time
import json
import requests
import urllib
# 修改默认编码
import sys
from bs4 import BeautifulSoup, Tag

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

def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print "---  new folder...  ---"
        print "---  OK  ---"

    else:
        print "---  There is this folder!  ---"

def mkdirAndPath(path):
    if not os.path.exists(path):
        f = open(path, 'w')
        print path
        f.close()
        print path + " created."
    else:
        print path + " already existed."
    return


from multiprocessing import Pool

if __name__ == '__main__':

    my_headers = [
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0""Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"]

    article_url_index_list = []
    #
    stockList = []
    file_name = 'annual.txt'

    with open(file_name, 'r') as read_list:
        read_list = read_list.readlines()

        resultsL = read_list.__len__()
        for x in range(0, resultsL):
            line = read_list[x]
            splits = line.split('#')
            code = (str)(splits[0])
            # print fieName
            stockList.append({'URL': code, 'NAME': (str)(splits[1])})

    for xx in stockList:

        for raw_front_page_index in range(1, 5):

            fileN = str(xx['NAME']).strip()
            uux = xx['URL']

            sdPath = '/Volumes/work/TGB/{}'.format(fileN)

            mkdir(sdPath)

            url = u"http://istock.jrj.com.cn/yanbao_{}_p{}.html"

            header = {'User-Agent': random.choice(my_headers),
                      }
            #

            content = requests.get(url.format(uux, raw_front_page_index), headers=header)
            soup = BeautifulSoup(content.text, 'lxml')

            list_p_list = soup.find_all('td', class_="left")
            for p in list_p_list:
                # print p

                list_pcyc_li = p.find_all('a')
                for li in list_pcyc_li:
                    xxurl = li.get('href')
                    # print xxurl

                    if not 'http://istock.jrj.com.cn/list,yanbao.html' == xxurl:

                        header = {'User-Agent': random.choice(my_headers)}
                        time.sleep(1)
                        result = requests.get(xxurl, headers=header)
                        # result = unicode(result.content, 'GBK').encode('UTF-8')

                        xxsoup = BeautifulSoup(result.text, 'lxml')

                        title_tationl = xxsoup.find_all('h1')
                        tt = str(title_tationl[0].text).strip()

                        xxlist_p_list = xxsoup.find_all('p', class_='title')[0]
                        xxlist_ds = xxsoup.find_all('span', class_='fr')[0]

                        realu = str(xxlist_p_list).replace(str(xxlist_ds), '', 1)

                        realuxsoup = BeautifulSoup(realu, 'lxml')

                        sp = str(realuxsoup.text).split(' ')

                        ttime = sp[1]

                        if ttime.__contains__('发表于'):
                            ttime = sp[2]

                        # print (sp[2]).text
                        # print (sp[3]).text

                        # print ttime

                        all_main = xxsoup.find_all('div', class_='main')[0]

                        realuxsoup = BeautifulSoup(str(all_main), 'lxml')

                        reaupp = realuxsoup.find_all('p')

                        for pp in reaupp:
                            list_pcyc_li = pp.find_all('a')

                            for li in list_pcyc_li:
                                print li.text
                                ttt =  li.get('href')

                                print ttt

                                fileName = u"{}_{}.pdf".format(ttime, str(li.text).replace('/',""))

                                basePath = '/Volumes/work/TGB/{}/{}'.format(fileN, fileName)

                                mkdirAndPath(basePath)

                                r = requests.get(ttt, stream=True)
                                with open(basePath, "wb") as pdf:
                                    for chunk in r.iter_content(chunk_size=1024):
                                        if chunk:
                                            pdf.write(chunk)
