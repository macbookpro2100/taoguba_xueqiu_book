# -*-encoding:utf-8-*-

'''
Author:     Super_Red
Date:       19/3/2017
Describe:   Download annal reports from the stock id
'''

import requests

from bs4 import BeautifulSoup
import re
import datetime

import time
import sys

reload(sys)

sys.setdefaultencoding('utf-8')


class downloader(object):
    def __init__(self):
        print 'start'



    def downloadFromID(self, stockID):
        reportList = self.findAnnalReports(stockID)
        for index, value in enumerate(reportList):
            # print("{index:3}:\t{date:2}\t{name}".format(index=index + 1, date=value[0], name=value[1]))
            # date_time = datetime.datetime.strptime(str(date=value[0]), '%Y-%m-%d')
            start = '2017-01-01'
            # 根据时间判断下载
            if str(value[0]) > start:
                reportIndex = index
                print("{name} downloading...................".format(name=reportList[reportIndex][1]))
                pdfUrl = self.findPDFUrl(reportList[reportIndex][2])
                self.downloadPDF(reportList[reportIndex][1], pdfUrl)

    def findAnnalReports(self, stockid):
        r = requests.get(
            "http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/{stockid}/page_type/ndbg.phtml".format(
                stockid=stockid))

        r = unicode(r.content, 'GBK').encode('UTF-8')
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
        r = requests.get(originUrl)
        r.encoding = "gbk"
        bsObj = BeautifulSoup(r.text, "html.parser")
        result = bsObj.findAll("a")
        pdf = [link["href"] for link in result if "PDF" in link["href"]][0]
        return pdf

    def downloadPDF(self, name, url, isDesktop=True):
        if isDesktop:
            fileName = "/Volumes/work/ink/ink_work/ppt/{name}.pdf".format(name=name)
        else:
            fileName = "{name}.pdf".format(name=name)
        pdf = requests.get(url, stream=True)
        with open(fileName, "wb") as file:
            for chunk in pdf:
                file.write(chunk)
        print("Done!")


if __name__ == '__main__':
    a = downloader()

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
        a.downloadFromID(xx)
