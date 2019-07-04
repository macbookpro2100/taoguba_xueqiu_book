# -*-encoding:utf-8-*-

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

reload(sys)

sys.setdefaultencoding('utf-8')


class AnnualReport(object):
    def __init__(self):
        print 'start'

    def start(self):

        stockList = []
        file_name = 'annual.txt'

        with open(file_name, 'r') as read_list:
            read_list = read_list.readlines()

            resultsL = read_list.__len__()
            for x in range(0, resultsL):
                line = read_list[x]
                splits = line.split('#')
                fieName = (str)(splits[0])
                # print fieName
                stockList.append(fieName)

        for xx in stockList:
            self.downloadFromID(xx)


    def compare_time(time1,time2):
        s_time = time.mktime(time.strptime(time1,'%Y-%m-%d'))
        e_time = time.mktime(time.strptime(time2,'%Y-%m-%d'))
        print 's_time is:',s_time
        print 'e_time is:',e_time
        return int(s_time) - int(e_time)


    def downloadFromID(self, stockID):
        reportList = self.findAnnalReports(stockID)
        for index, value in enumerate(reportList):
            # print("{index:3}:\t{date:2}\t{name}".format(index=index + 1, date=value[0], name=value[1]))
            # date_time = datetime.datetime.strptime(str(date=value[0]), '%Y-%m-%d')
            d1 = datetime.datetime.strptime(str(value[0]), '%Y-%m-%d')
            d2 = datetime.datetime.strptime('2017-01-01', '%Y-%m-%d')
            delta = d1 - d2

            # 根据时间判断下载
            if delta.days > 1:
                reportIndex = index
                print("{name} downloading...................".format(name=reportList[reportIndex][1]))
                pdfUrl = self.findPDFUrl(reportList[reportIndex][2])
                self.downloadPDF(reportList[reportIndex][1], pdfUrl)

    def findAnnalReports(self, stockid):
        url = u"http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/{stockid}/page_type/ndbg.phtml".format(
                stockid=stockid)
        r = Http.get_content(url)
        r = unicode(r, 'GBK').encode('UTF-8')
        bsObj = BeautifulSoup(r, "html.parser")
        result = bsObj.findAll("div", {"class": "datelist"})[0]
        dateList = re.findall('\d{4}-\d{2}-\d{2}', result.text)
        returnList = []
        for index, value in enumerate(result.findAll("a")):
            returnList.append([dateList[index], value.text, "http://vip.stock.finance.sina.com.cn" + value["href"]])
        return returnList

    def findPDFUrl(self, originUrl):
        '''
            the links returned from the method <findAnnalReports> are not the PDF links
            those origin links should be further excavated to find the true links
        '''
        r = Http.get_content(originUrl)
        # r.encoding = "gbk"
        # result = unicode(str(result), 'GBK').encode('UTF-8')
        bsObj = BeautifulSoup(r, "html.parser")
        result = bsObj.findAll("a")
        pdf = [link["href"] for link in result if "PDF" in link["href"]][0]
        return pdf

    def downloadPDF(self, name, url, isDesktop=True):
        if isDesktop:
            fileName = "/ink/work/62/ink/{name}.pdf".format(name=name)
        else:
            fileName = "{name}.pdf".format(name=name)

        if not os.path.exists(fileName):    
           pdf = Http.get_content(url, timeout=180)
           with open(fileName, "wb") as file:
               for chunk in pdf:
                   file.write(chunk)
           print("Done!")
