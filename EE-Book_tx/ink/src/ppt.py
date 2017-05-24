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

reg = re.compile(r'<h4( class="status-title")?>(.*)</h4>(.*)</script>(.*)<!-- pdf--></div>')
imgreg = re.compile('<img( class="lazy")? data-original="(.*?)"')
imgnamereg = re.compile('/([0-9a-z]+?\.(jpg|png))')

THeaders = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'd_c0="AEBAIWd4ygqPThA-2NT1dyOH3dAKgpSHu5M=|1478166245"; q_c1=1a0cbff6d19145d2bf76cb7e509b06e9|1478166245000|1478166245000; l_cap_id="YWE0NDg1YWQ5M2FmNDQ2NThkODAzYzkzMWQxMGI2MjQ=|1478166245|00a0a16b878d9a92b61b3feb9325165df20d27ce"; cap_id="MWIzZjBkZWM2ZDM0NDJjMGIxZTIyMTBlNTQ5N2IxOGI=|1478166245|18ffc2d6c77b121aab8957e40e4b445f7f085002"; _zap=6262b4bc-19c5-47a7-801a-faaa713c5e72; login="Mzk0NGY0MTdlNDQzNDZiMWJhODJlMzQzMjgyZDI4NjM=|1478166249|ec49d92744f4e96c344914c6729f8a88d0f733b3"; _xsrf=a97a0314cd0ef5bdaa2673615158e47f; s-q=%E5%93%81%E7%89%8C; s-i=1; sid=ovm436bg; s-t=autocomplete; __utmt=1; __utma=51854390.1179030424.1479882854.1479882854.1479882854.1; __utmb=51854390.2.10.1479882854; __utmc=51854390; __utmz=51854390.1479882854.1.1.utmcsr=36zhen.com|utmccn=(referral)|utmcmd=referral|utmcct=/t; __utmv=51854390.100-1|2=registration_date=20110826=1^3=entry_date=20110826=1; z_c0=Mi4wQUFCQVlhWVlBQUFBUUVBaFozaktDaGNBQUFCaEFsVk42Wk5DV0FEdWxwVnVVOHdYSTZiUExuMXk4NzJGT3hsdVJR|1479882853|b46e709fe8f3bcfcf6a4c1ed53c91fcb8392af61',
    'Host': 'www.zhihu.com',
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


if __name__ == '__main__':

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

    f = open(u'TGB_List页面.txt', 'a')
    for i in range(0, 1):
        url = u"https://www.zhihu.com/question/25541287"
        r = requests.get(url.format(i), headers=THeaders)
        # print r
        soup = BeautifulSoup(r.text,'lxml')

        list_p_list = soup.find_all('div', class_="zm-editable-content clearfix")
        for p in list_p_list:
            print p

            list_pcyc_li = p.find_all('a',class_ ="internal")
            for li in list_pcyc_li:
                # print li

                print li.text
                print li.get('href')

                f.write(u'{} #{}\n'.format(li.get('href'),li.text ))
    f.close()
