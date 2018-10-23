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

    url = u"http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&js=var%20xAqhaJyq={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&ps=25&p=6&code=601318&rt=51250843"



    header = {'User-Agent': random.choice(my_headers)}
    #
    # sdt = str((int(time.time() / 30)))
    #
    # dfg = url.replace("{##}", sdt, 1)




    content = requests.get(url, headers=header)

    if content:
        jsonD = str(content.content).split('=')[-1]

        jdata = json.loads(jsonD)
        articles = jdata['data']
        for article in articles:
            rticlet = article['datetime']

            date_time = datetime.datetime.strptime(rticlet, '%Y-%m-%dT%H:%M:%S')
            destU = u"http://data.eastmoney.com/report/{}/{}.html ".format(date_time.strftime('%Y%m%d'),
                                                                           article['infoCode'])

            header = {'User-Agent': random.choice(my_headers)}
            result = requests.get(destU, headers=header)
            result = unicode(result.content, 'GBK').encode('UTF-8')

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

            fileName = u"{}_{}_{}_{}.pdf".format(ttime, (sp[2]).text, tt, (sp[3]).text)
            # 时间 券商 名称  author

            print fileName

            urlsp = sp[-1]

            basePath = '/Volumes/work/TGB/平安/{}'.format(fileName)

            # 创建文件夹

            list_pcyc_li = urlsp.find_all('a')
            for li in list_pcyc_li:
                ttt = li.get('href')
                mkdirAndPath(basePath)
                print ttt
                r = requests.get(ttt, stream=True)
                with open(basePath, "wb") as pdf:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            pdf.write(chunk)
