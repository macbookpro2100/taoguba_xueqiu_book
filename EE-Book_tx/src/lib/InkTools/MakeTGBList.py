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

import sys
from bs4 import BeautifulSoup

from src.tools.http import Http
from src.tools.path import Path


reload(sys)

sys.setdefaultencoding('utf-8')

reg = re.compile(r'<h4( class="status-title")?>(.*)</h4>(.*)</script>(.*)<!-- pdf--></div>')
imgreg = re.compile('<img( class="lazy")? data-original="(.*?)"')
imgnamereg = re.compile('/([0-9a-z]+?\.(jpg|png))')

TGBHeaders = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'UM_distinctid=16a09d56380fe-001f41eddcd37e-163b6952-13c680-16a09d56381dcc; JSESSIONID=c10fab5d-77c5-45eb-9a1e-350efd4628aa; CNZZDATA1574657=cnzz_eid%3D1083744182-1554938916-%26ntime%3D1556182433; Hm_lvt_cc6a63a887a7d811c92b7cc41c441837=1554943143,1555980522,1556185682; notActiveUserIDPC=47884370; tgbuser=929400; tgbpwd=034188E14447lc8hzuwuiqmwsh; Hm_lpvt_cc6a63a887a7d811c92b7cc41c441837=1556186526',
    'Host': 'www.taoguba.com.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

XueQiuHeaders = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'xq_a_token=ffa7b19c02a198620f85b3d9d7a93af9939d3eef; bid=140b75475571da90d7d573a14ca9957a_is5c7shi;',
    'Host': 'xueqiu.com',
    'Pragma': 'no-cache',
    'RA-Sid': 'DE49C559-20141120-021811-7a9e85-d30286',
    'RA-Ver': '2.8.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36'
}


def Mkdir(DirName=u''):  # PassTag
    if DirName == '':
        return
    else:
        try:
            os.mkdir(DirName)
        except  OSError:
            pass  # 已存在
    return


def getTGBAticle():
    f = open(u'TGB_List页面.txt', 'a')
    url = u"http://www.taoguba.com.cn/best?pageNo={}&blockID=0&flag=0"
    tagrList = {}

    for i in range(0, 400):
        r = requests.get(url.format(i), headers=TGBHeaders)

        soup = BeautifulSoup(r.text)
        # f.write(u'  精华 第{}页\n'.format(i))
        list_p_list = soup.find_all('div', class_="p_list01")
        for p in list_p_list:
            # print p
            # 回帖/浏览
            list_pcyc_l_4 = p.find_all('li', class_="pcdj04")[0]
            liuyan_num = int(str(list_pcyc_l_4.text).split('/')[-1])
            huitie_num = int(str(list_pcyc_l_4.text).split('/')[-2])
            # print liuyan_num
            # 加油
            list_pcyc_l_5 = p.find_all('li', class_="pcdj05")[0]
            jiayou_num = int(str(list_pcyc_l_5.text).split('/')[-1])
            # print jiayou_num
            # 推荐
            list_pcyc_l_5_1 = p.find_all('li', class_="pcdj05")[1]
            tuijian_num = int(str(list_pcyc_l_5_1.text).split('/')[-1])
            # print tuijian_num

            # if liuyan_num > 200000 or jiayou_num > 100 or tuijian_num > 800:
            # 100万阅读  or  7000回帖
            # if   (huitie_num > 7000 and liuyan_num > 1500000):
            if  tuijian_num > 280:
                list_pcyc_l_02 = p.find_all('li', class_="pcdj02")

                # list_pcyc_l_ = list_pcyc_l_02.find_all('li', class_="pcdj02")
                for tgo_right in list_pcyc_l_02:
                    for link in tgo_right.findAll('a'):
                        # print link.get('href')
                        # url_0 = u'http://www.taoguba.com.cn/{}'.format(link.get('href'))
                        # tarUrl = url_0
                        # r = requests.get(url_0, headers=TGBHeaders)
                        # # print r.text
                        # dom = BeautifulSoup(r.text, "lxml")
                        # list_pcyc_l_ = dom.find_all('div', class_="left t_page01")
                        # try:
                        #     for tgo_tgo_ in list_pcyc_l_:
                        #         linkl = tgo_tgo_.findAll('a')
                        #         tarUrl = linkl[0].get('href')
                        #         print tarUrl.split('/')[3]
                        # except  IndexError as   e:
                        #     tarUrl = url_0
                        #     continue

                        lllk= link.get('href')
                        lk= str(lllk).split('/')[1]

                        wt  = u'http://www.taoguba.com.cn/Article/{}/0 #{}\n'.format(lk, link.get('title'))

                        print wt
                        f.write(wt)


                        tagrList.update({wt:huitie_num})
                        print link.get('title')
                        # f.write(u'\n\n\n')

    #排序

    #
    # L = sorted(tagrList.items(),key=lambda item:item[1])
    #
    #
    #
    # #
    # for xd in  L:
    #     # print xd
    #     f.write(str(xd))
    f.close()


def reloadtocatch():
    rootdir = "/Volumes/MacintoshHD/TC/todo"  # 指明被遍历的文件夹
    filelist = os.listdir(rootdir)
    ff = open('TGB_List.txt', 'w')
    for file in filelist:
        print file
        # if file.startswith('TGB'):
        article_id = (str(file).split('_')[-1]).strip(')')
        print article_id
        # tagrId = u"http://www.taoguba.com.cn/Article/{}/0\n".format(article_id)
        tagrId = u"https://www.huxiu.com/{}\n".format(article_id)
        ff.write(tagrId)

    # 图片文件夹
    rootdir = "/Volumes/MacintoshHD/TC/todo"  # 指明被遍历的文件夹
    picdir = "/Volumes/MacintoshHD/TC/picture"
    filelist = os.listdir(rootdir)
    ff = open('TGB_List.txt', 'w')
    for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        # for dirname in dirnames:  # 输出文件夹信息
        #     # print "parent is: " + parent
        #     print  "dirname is: " + dirname

        for filename in filenames:  # 输出文件信息
            print "parent is :" + parent
            print "filename is:" + filename
            print "the full name of the file is:" + os.path.join(parent, filename)  # 输出文件路径信息

            if filename.endswith('jpg'):
                Path.copy(os.path.join(parent, filename), picdir)

    # for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    #     for dirname in dirnames:  # 输出文件夹信息
    #     #     # print "parent is: " + parent
    #         print  "dirname is: " + dirname
    #
    #     # for filename in filenames:  # 输出文件信息
    #     #     print "parent is :" + parent
    #     #     print "filename is:" + filename
    #     #     print "the full name of the file is:" + os.path.join(parent, filename)  # 输出文件路径信息
    ff.close()


class MakeHelp(object):
    def __init__(self):
        #   初始化目录结构

        return

    def start(self):
        print 'start RecentHelp'
    # f = open('TGB_List页面.txt', 'r')
    # ff = open('TGB_List.txt', 'w')
    # for eachLine in f:
    #     ll = eachLine.split('#')
    #     if len(ll) > 1:
    #         ff.write(eachLine)
    #     else:
    #         print ll
    #
    # f.close()
    # ff.close()


    # ff = open('/Users/li/Desktop/list1.txt', 'w')
    #
    # baseU = "file 'segment{}_7_av.ts'\n"
    # for page in range(1, 251):
    #
    #           ff.write(baseU.format(page))
    #
    #
    # ff.close()




    # reloadtocatch()



    # for i in range(1,1688):
    #     print  str(i) +" "+ str(i/10) +" "+ str(i%10)
    #
    #
    # str = '<a href="blog/1571532" onmouseout="offTip()" onmouseover="userTips(this,1571532);" target="_blank">xhj4555660</a>'
    # print  clearAuuA(str)
    # htp='http://image.taoguba.com.cn/img/2016/04/19/wq3fb28kcslb.png@!topic'
    # print  '文件名是'+  htp.split('/')[-1]
    #
    #
    #获取
    # getTGBAticle()

    # start = 1990
    # end = 2018
    # last_tatal = 10000
    # for i in range(start,2018):
    #     last_tatal = last_tatal *(1 + 0.2)
    # print last_tatal
    #









