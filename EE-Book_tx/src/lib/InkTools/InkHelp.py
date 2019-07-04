# -*- coding: utf-8 -*-
import os
import sqlite3

from src.tools.debug import Debug
import sys
from bs4 import BeautifulSoup
import os
import re
import time
import json
from src.tools.http import Http
from src.tools.path import Path

from jrj_report import JRJ_Report
from dc_report import DC_Report
from annual_report import AnnualReport
from MakeTGBList import MakeHelp
from dc_report import LAYJ_Report


class RecentHelp(object):
    def __init__(self):
        #   初始化目录结构

        return

    def start(self):
        print 'start RecentHelp'

        # helper = JRJ_Report()
        # helper.start()

        # helper = DC_Report()
        # helper = DFCF_Report()
        # helper = LAYJ_Report()
        # helper.start()

        # helper = AnnualReport()
        # helper.start()
        #
        # hh = LAYJ_Report()
        # hh.start()


class InkHelp(object):
    def __init__(self):
        #   初始化


        return

    def start(self):
        print 'start InkHelp'

        helper = JRJ_Report()
        helper.start()
        #
        # helper = MakeHelp()
        # helper = DC_Report()
        # helper.start()

        # helper = AnnualReport()
        # helper.start()
        #
        # hh = Recent_Report()
        # hh.start()


        # fileP = '/Volumes/MacintoshHD/YunDowdload/ink/医药行业'
        # distP = '/Users/ink/Desktop/temp'
        #
        # filenames = os.listdir(fileP)
        #
        # for fileN in filenames:
        #
        #
        #     if str(fileN).__contains__('周报') or str(fileN).__contains__('川财') or str(fileN).__contains__('或'):
        #     # if str(fileN).__contains__('快报') or str(fileN).__contains__('点评') or str(fileN).__contains__('或'):
        #     # if str(fileN).__contains__('安信证券') or str(fileN).__contains__('东北证券') or str(fileN).__contains__('或'):
        #         print fileN
        #         srcP = fileP + '/' + fileN
        #
        #         os.remove(srcP)








class TODAY_Report(object):
    def __init__(self):
        #   初始化目录结构

        return

    def start(self):
        print 'start JRJ_Report'

        stockList = []

        stockList.append({'URL': '1', 'NAME': '宏观研究'})
        # stockList.append({'URL': '8', 'NAME': '策略趋势'})

        for xx in stockList:

            for raw_front_page_index in range(5, 50):

                print '开始第' + str(raw_front_page_index) + '页面 下载'

                fileN = str(xx['NAME']).strip()
                uux = xx['URL']

                sdPath = ' /Volumes/MacintoshHD/File/{}'.format(fileN)

                Path.mkdir(sdPath)

                url = u"http://istock.jrj.com.cn/yanbao_{}_p{}.html"

                request_url = url.format(uux, raw_front_page_index)
                content = Http.get_content(request_url)

                soup = BeautifulSoup(content, 'html.parser')

                list_p_list = soup.find_all('div', class_="yb_con")

                for p in list_p_list:
                    # print p

                    list_pcyc_li = p.find_all('a')
                    for li in list_pcyc_li:
                        xxurl = li.get('href')
                        # print xxurl

                        if not 'http://istock.jrj.com.cn/list,yanbao.html' == xxurl:

                            try:

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

                                        # print ttt

                                        ftype = 'pdf'

                                        if str(ttt).endswith('.xlsx'):
                                            ftype = 'xlsx'

                                        fileName = u"{}_{}.{}".format(ttime, str(li.text).replace('/', ""), ftype)

                                        print fileName

                                        basePath = '/ink/work/62/ink/{}/{}'.format(fileN, fileName)

                                        Path.mkdirAndPath(basePath)

                                        Debug.print_in_single_line(u'开始下载   {}  '.format(ttt))
                                        if ttt:
                                            content = Http.get_content(url=ttt, timeout=180)
                                            if not content:
                                                # Debug.logger.debug(u'文件『{}』下载失败'.format(ttt))
                                                content = ''
                                            else:
                                                Debug.print_in_single_line(u'文件 {} 下载完成'.format(ttt))
                                        else:
                                            #   当下载地址为空的时候，就没必要再去下载了
                                            content = ''
                                        if not os.path.exists(fileName):
                                            if content.__len__() > 10:
                                                with open(basePath, "wb") as pdf:
                                                    pdf.write(content)
                            except Exception as e:
                                print 'Exception ' + e.message


class Recent_Report(object):
    def __init__(self):
        #   初始化目录结构

        return

    def start(self):
        print 'start JRJ_Report'

        stockList = []
        stockList.append({'URL': '8', 'NAME': '风险'})
        # stockList.append({'URL': '1', 'NAME': '风险'})
        # stockList.append({'URL': '1', 'NAME': '宏观研究'})

        for xx in stockList:

            for raw_front_page_index in range(1, 3000):
            # for raw_front_page_index in range(1, 2):

                print '开始第' + str(raw_front_page_index) + '页面 下载'

                fileN = str(xx['NAME']).strip()
                uux = xx['URL']

                sdPath = '/ink/work/62/ink/{}'.format(fileN)

                Path.mkdir(sdPath)

                url = u"http://istock.jrj.com.cn/yanbao_{}_p{}.html"

                request_url = url.format(uux, raw_front_page_index)
                content = Http.get_content(request_url)

                soup = BeautifulSoup(content, 'html.parser')

                list_p_list = soup.find_all('div', class_="yb_con")

                for p in list_p_list:
                    # print p

                    list_pcyc_li = p.find_all('a')
                    for li in list_pcyc_li:


                        xxurl = li.get('href')
                        # print xxurl

                        preTitle = li.get('title')

                        # print preTitle

                        toDownload = str(preTitle).__contains__('日本')

                        if not 'http://istock.jrj.com.cn/list,yanbao.html' == xxurl and toDownload:

                            print preTitle

                            try:

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

                                        # print ttt

                                        ftype = 'pdf'

                                        if str(ttt).endswith('.xlsx'):
                                            ftype = 'xlsx'
                                        if str(ttt).endswith('.docx'):
                                            ftype = 'docx'
                                        fileName = u"{}_{}.{}".format(ttime, str(li.text).replace('/', ""), ftype)

                                        print fileName

                                        basePath = '/ink/work/62/ink/{}/{}'.format(fileN, fileName)

                                        Path.mkdirAndPath(basePath)

                                        Debug.print_in_single_line(u'开始下载   {}  '.format(ttt))
                                        if ttt:
                                            content = Http.get_content(url=ttt, timeout=180)
                                            if not content:
                                                # Debug.logger.debug(u'文件『{}』下载失败'.format(ttt))
                                                content = ''
                                            else:
                                                Debug.print_in_single_line(u'文件 {} 下载完成'.format(ttt))
                                        else:
                                            #   当下载地址为空的时候，就没必要再去下载了
                                            content = ''
                                        if not os.path.exists(fileName):
                                            if content.__len__() > 10:
                                                with open(basePath, "wb") as pdf:
                                                    pdf.write(content)
                            except Exception as e:
                                print('next')





class BerkshireHathaway(object):
    def __init__(self):
        #   初始化目录结构
        return

    def start(self):
        print 'start JRJ_Report'

        f = open('TGB_List.txt', 'w')
        # f = open('buffett.txt', 'w')
        url = u"https://buffett.cnbc.com/annual-meetings/"
        r = Http.get_content(url)
        # print r.text
        soup = BeautifulSoup(r.text, 'lxml')

        list_p_list = soup.find_all('div', class_="SectionTiles-gridItem")
        for p in list_p_list:
            # print p

            list_pcyc_li = p.find_all('a')
            for li in list_pcyc_li:

                # print li.text
                xxurl = li.get('href')
                # deep level

                xxr = Http.get_content(xxurl)
                # print r.text
                xxsoup = BeautifulSoup(xxr.text, 'lxml')

                xxlist_p_list = xxsoup.find_all('div',
                                                class_="Column-buffett Column-rectangleLeadRight Column-squareLeadRight ")

                for x in range(0, 1):
                    xd = xxlist_p_list[x]
                    xdli = xd.find_all('a')
                    for xli in xdli:
                        ddurl = xli.get('href')
                        print ddurl


                        ddr = Http.get_content(ddurl)

                        ssss= str(ddr.content)

                        # print ssss

                        regexpr=re.compile(r"playbackURL(.*?)m3u8",re.DOTALL)
                        regexpr2=re.compile(r"m3u8(.*?)transcript",re.DOTALL)
                        result=regexpr.search(ssss)
                        result2=regexpr2.search(ssss)
                        try:
                            ss =  result.group(1)

                            s = ss.replace('\u002F','/',100)

                            sreal = s[3:-8]
                            print sreal


                            title =  result2.group(1)
                            title =  title[11:-3]

                            resultStr = u"{}#https:{}/index_7_av.m3u8?null=0\n".format(title,sreal)

                            print resultStr
                            f.write(str(resultStr))

                        except:
                            print "Can't find match string"


        f.close()






        # lds= ssss.split('playbackURL')
        # for ld in lds :
        #     print ld



        # url = u"http://onboarding.sf-rush.com/driver/finish"
        # r = requests.get(url, headers=SFHeaders)
        # print r.text

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

        # f = open(u'TGB_List页面.txt', 'a')
        # for i in range(0, 1):
        #     url = u"https://www.zhihu.com/question/25541287"
        #     r = requests.get(url.format(i), headers=THeaders)
        #     # print r
        #     soup = BeautifulSoup(r.text,'lxml')
        #
        #     list_p_list = soup.find_all('div', class_="zm-editable-content clearfix")
        #     for p in list_p_list:
        #         print p
        #
        #         list_pcyc_li = p.find_all('a',class_ ="internal")
        #         for li in list_pcyc_li:
        #             # print li
        #
        #             print li.text
        #             print li.get('href')
        #
        #             f.write(u'{} #{}\n'.format(li.get('href'),li.text ))
        # f.close()
