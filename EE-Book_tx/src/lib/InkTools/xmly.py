# -*- coding: utf-8 -*-
# coding=utf-8
import sys
import urllib2
import json
import os

# from lxml import etree  #可实现xpath
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


# 抓取喜马拉雅音频文件 网址：https://www.ximalaya.com/top/
class XiMa(object):
    def __init__(self, bookName, bookId):
        self.bookId = bookId
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
        }

        self.bookName = bookName

    # 获取当前频道资源列表
    def getSource(self, numberIndx):
        startUrl = "https://www.ximalaya.com/revision/play/album?albumId={}&pageNum={}&sort=-1&pageSize=30".format(
            int(self.bookId), numberIndx)

        req = urllib2.Request(startUrl, headers=self.headers)
        response = urllib2.urlopen(req)
        result = response.read().decode()
        jsonResult = json.loads(result)
        dataList = jsonResult['data']['tracksAudioPlay']
        sourceList = []
        for item in dataList:
            source = {}
            source['name'] = item['trackName']
            source['src'] = item['src']
            sourceList.append(source)
        # print(sourceList)
        return sourceList

    # 保存音频文件
    def saveSource(self, sources):
        # bookName =str(self.bookName).replace('"',' ')  # ??未起作用
        path = u'/ink/work/62/{}'.format(self.bookName)
        isExistd = os.path.exists(path)
        # 判断文件夹是否存在
        if not isExistd:
            os.makedirs(path)

        for item in sources:
            print('开始抓取文件[' + item['name'] + ']...')
            filePath = path + '/{}.m4a'.format('[' + self.bookName + ']' + item['name'])
            # 判断文件是否存在
            if os.path.exists(filePath):
                print("已存在！无需下载")
                continue

            # 以二进制格式打开
            f = open(filePath, 'ab')
            req = urllib2.Request(item['src'], headers=self.headers)
            response = urllib2.urlopen(req)
            r = response.read()

            f.write(r)
            f.close()
            print('文件[' + item['name'] + ']抓取结束')

    # 执行方法
    def runFun(self,maxNun):

        for raw_front_page_index in range(15, maxNun + 1):
            sourceList = self.getSource(raw_front_page_index)
            self.saveSource(sourceList)


# 获取所有频道信息
def getAllPDList():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    mainUrl = "https://www.ximalaya.com/revision/rank/getRankList?rankType=freeAlbum&pageSize=100"  # 顶级入口目录
    req = urllib2.Request(mainUrl, headers=headers)
    response = urllib2.urlopen(req)
    result = response.read().decode()
    result = json.loads(result)
    dataList = result['data']['freeAlbumRank']['rankListInfo']
    dataSources = []
    for data in dataList:
        dataSource = {}
        dataSource['id'] = data['id']
        dataSource['title'] = data['albumTitle']
        dataSources.append(dataSource)
    return dataSources


# 调用入口
if __name__ == '__main__':
    # xima=XiMa('华为是560亿美元的小草',3114422)
    # xima=XiMa('雷军：重温那些雷人雷语',3117870)
    # xima=XiMa('马云：不拼爹不行贿',3114415)
    # xima=XiMa('雷军演讲全集',3580509)
    # xima=XiMa('巴菲特100句投资经典语录',6309826)
    # xima=XiMa('李书福演讲全集',3575921)
    # xima=XiMa('郭台铭演讲全集',3575600)
    # xima=XiMa('张小龙演讲',3574575)
    # xima=XiMa('知行合一：王阳明',2673722)
    xima = XiMa('白话《资治通鉴》', 6268204)
    xima.runFun(34)

    # allSources = getAllPDList()
    # #print(allSources)
    # for source in allSources:
    #     xima=XiMa(source['title'],source['id'])
    #     xima.runFun()
