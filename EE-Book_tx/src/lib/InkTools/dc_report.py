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
from src.tools.match import Match

reload(sys)

sys.setdefaultencoding('utf-8')

import random
import json
import time
import datetime

from src.tools.path import Path
from multiprocessing import Pool


class DC_Report(object):
    def __init__(self):
        #   初始化目录结构

        return

    def start(self):
        print 'start 东财研报'

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
            for raw_front_page_index in range(1, 5):
                fileN = str(xx['NAME']).strip()
                uux = xx['URL']

                sdPath = '/ink/work/62/ink/{}'.format(fileN)
                Path.mkdir(sdPath)
                # url = u"http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&js=var%20LhAYbcgn={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&ps=25&p=1&code=000333&rt=51734025"

                burl = u"http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&js=var%20LhAYbcgn={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&ps=25&"
                uu = u"p={0}&code={1}&rt="

                url = '%s%s' % (burl, uu.format(raw_front_page_index, uux))

                content = Http.get_content(url)

                if content:
                    jsonD = str(content).split('=')[-1]

                    jdata = json.loads(jsonD)
                    articles = jdata['data']
                    for article in articles:
                        rticlet = article['datetime']

                        date_time = datetime.datetime.strptime(rticlet, '%Y-%m-%dT%H:%M:%S')
                        destU = u"http://data.eastmoney.com/report/{}/{}.html ".format(date_time.strftime('%Y%m%d'),
                                                                                       article['infoCode'])

                        result = Http.get_content(destU)
                        result = unicode(result, 'GBK').encode('UTF-8')

                        xxsoup = BeautifulSoup(result, 'html.parser')

                        title_tationl = xxsoup.find_all('h1')
                        tt = str(title_tationl[0].text).strip()

                        xxlist_p_list = xxsoup.find_all('div', class_='report-infos')[0]

                        sp = xxlist_p_list.find_all('span')

                        ttime = str((sp[1]).text)

                        date_time = datetime.datetime.strptime(ttime, '%Y年%m月%d日 %H:%M')

                        # print date_time.strftime('%Y-%m-%d')

                        ttime = date_time.strftime('%Y-%m-%d')

                        # print (sp[2]).text
                        # print (sp[3]).text

                        title = Match.replace_specile_chars(tt)
                        title = title.replace('/', '', 100)

                        fileName = u"{}_{}_{}_{}.pdf".format(ttime, (sp[2]).text, title, (sp[3]).text)
                        # 时间 券商 名称  author

                        print fileName

                        urlsp = sp[-1]

                        basePath = '{}/{}'.format(sdPath, fileName)

                        # print basePath

                        # 创建文件夹

                        list_pcyc_li = urlsp.find_all('a')
                        for li in list_pcyc_li:
                            ttt = li.get('href')
                            Path.mkdirAndPath(basePath)
                            print ttt

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


class DFCF_Report(object):
    def __init__(self):
        #   初始化目录结构

        return

    def start(self):
        print 'start 东财股吧 研报'

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
            for raw_front_page_index in range(1, 3):
                fileN = str(xx['NAME']).strip()
                uux = xx['URL']

                sdPath = '/ink/work/62/ink/{}'.format(fileN)
                Path.mkdir(sdPath)

                burl = u"http://guba.eastmoney.com/list,{},2,f_{}.html"

                content = Http.get_content(burl.format(uux, raw_front_page_index))

                xxsoup = BeautifulSoup(content, 'html.parser')

                tagrt = xxsoup.find_all('div', id='articlelistnew')[0]

                ols = tagrt.find_all('div', class_='articleh normal_post')
                olss = tagrt.find_all('div', class_='articleh normal_post odd')

                splicy = []

                for xxos in ols:
                    splicy.append(xxos)
                for xx in olss:
                    splicy.append(xxos)

                for inkl in splicy:

                    try:

                        inklinkl = BeautifulSoup(str(inkl), 'html.parser')

                        spp = inklinkl.find_all('span', class_='l3')[0]

                        list_pcyc_li = spp.find_all('a')
                        for li in list_pcyc_li:
                            ttt = li.get('href')

                            print ttt

                            destU = u'http://guba.eastmoney.com{}'.format(ttt)

                            result = Http.get_content(destU)
                            # result = unicode(result, 'GBK').encode('UTF-8')

                            xxsoup = BeautifulSoup(result, 'html.parser')

                            title_tationl = xxsoup.find_all('div', id='zwconttbt')
                            tt = str(title_tationl[0].text).strip()
                            print tt

                            title = Match.replace_specile_chars(tt)
                            title = title.replace('/', '', 100)

                            title = title.replace('查看原文', '')

                            ttime = xxsoup.find_all('p', class_='publishdate')[0]

                            tttttime = str(ttime.text)[-10:]

                            print  tttttime

                            date_time = datetime.datetime.strptime(tttttime, '%Y-%m-%d')

                            # print date_time.strftime('%Y-%m-%d')

                            ttime = date_time.strftime('%Y-%m-%d')

                            fileName = u"{}_{}.pdf".format(ttime, title)
                            # 时间 券商 名称  author

                            print fileName

                            basePath = '{}/{}'.format(sdPath, fileName)

                            # print basePath

                            # 创建文件夹
                            #

                            spx = xxsoup.find_all('span', class_='zwtitlepdf')[0]

                            pdfu = spx.find_all('a')
                            for li in pdfu:
                                ttt = li.get('href')

                                print ttt
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
                    except Exception as e:
                        print('next')


class LAYJ_Report(object):
    def __init__(self):
        #   初始化目录结构

        return

    def start(self):
        print ' 中文研报 '

        stockList = []


        for raw_front_page_index in range(1, 251):
            fileN = '策略'

            sdPath = '/ink/work/62/ink/{}'.format(fileN)
            Path.mkdir(sdPath)

       #    http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=HGYJ&cmd=4&code=&ps=50&p=2&js=var%20UxmjGoYW={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&
            burl = u"http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=CLBG&cmd=4&code=&ps=50&p="
            # burl = u"http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=HGYJ&cmd=4&code=&ps=50&p="
            uu = u"&js=var%20GdYXcAjX={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&"

            url = '%s%s%s' % (burl, str(raw_front_page_index), uu)

            # print url

            content = Http.get_content(url)

            if content:
                try:
                    jsonD = str(content).split('=')[-1]

                    jdata = json.loads(jsonD)
                    articles = jdata['data']
                    for article in articles:

                        xxxs = str(article).split(',')
                        rticlet = xxxs[0]

                        preTitle = xxxs[5]

                        if str(preTitle).__contains__('川财') or str(preTitle).__contains__('或'):
                           continue

                        # if str(preTitle).__contains__('历史') or str(preTitle).__contains__('周期')or str(preTitle).__contains__('成长'):
                        # if str(preTitle).__contains__('政治') or str(preTitle).__contains__('中央经济')or str(preTitle).__contains__('贸易战'):
                        if str(preTitle).__contains__('日本'):
                            print preTitle
                            date_time = datetime.datetime.strptime(rticlet, '%Y/%m/%d %H:%M:%S')

                            infoCode = xxxs[1]
                            destU = u"http://data.eastmoney.com/report/{}/cl,{}.html ".format(
                                date_time.strftime('%Y%m%d'), infoCode)

                            print destU

                            result = Http.get_content(destU)
                            result = unicode(result, 'GBK').encode('UTF-8')

                            xxsoup = BeautifulSoup(result, 'html.parser')

                            title_tationl = xxsoup.find_all('h1')
                            tt = str(title_tationl[0].text).strip()

                            xxlist_p_list = xxsoup.find_all('div', class_='report-infos')[0]

                            sp = xxlist_p_list.find_all('span')

                            ttime = str((sp[1]).text)

                            date_time = datetime.datetime.strptime(ttime, '%Y年%m月%d日 %H:%M')

                            # print date_time.strftime('%Y-%m-%d')

                            ttime = date_time.strftime('%Y-%m-%d')

                            # print (sp[2]).text
                            # print (sp[3]).text

                            title = Match.replace_specile_chars(tt)
                            title = title.replace('/', '', 100)

                            fileName = u"{}_{}_{}_{}.pdf".format(ttime, (sp[2]).text, title, (sp[3]).text)
                            # 时间 券商 名称  author

                            print fileName

                            urlsp = sp[-1]

                            basePath = '{}/{}'.format(sdPath, fileName)

                            # print basePath

                            # 创建文件夹

                            list_pcyc_li = urlsp.find_all('a')
                            for li in list_pcyc_li:
                                ttt = li.get('href')
                                Path.mkdirAndPath(basePath)
                                print ttt

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



                except Exception as e:
                    print('next')
