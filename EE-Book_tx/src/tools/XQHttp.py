# -*- coding: utf-8 -*-

import os
import traceback
import urllib2
import urllib
import socket  # 用于捕获超时错误
import zlib
import cookielib  # 用于生成cookie
import time
import json
import requests
import urllib

from config import Config
from db import DB
from debug import Debug

# header = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate, sdch, br',
#     'Accept-Language': 'zh-CN,zh;q=0.8',
#     'Connection': 'keep-alive',
#     'Cookie': 'aliyungf_tc=AQAAAMsKzEyWuQMAs+US2phsoYwEpulG; xq_a_token.sig=c0ca-9ydxJfWBWHWuDP7p-WHNmE; xq_r_token.sig=L_Wf0-2063SwurwmV9iJTdu0yCI; _ga=GA1.2.52300829.1556447956; _gid=GA1.2.1933846687.1556447956; device_id=0bff3e76a9073b36641b139f7880269f; Hm_lvt_1db88642e346389874251b5a1eded6e3=1556447957; s=ee11hc9brl; xq_a_token=ec6dc91a20449fb627b0cb35b417cbbe35571dd0; xqat=ec6dc91a20449fb627b0cb35b417cbbe35571dd0; xq_r_token=0e5956f7b8ea80f7bc9249345db8ca3d3e22b65d; xq_token_expire=Thu%20May%2023%202019%2018%3A40%3A25%20GMT%2B0800%20(CST); xq_is_login=1; u=3405123156; bid=145ffe6154eaf248e7c3f639c59514fa_jv0sz3mk; snbim_minify=true; _gat=1; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1556448352',
#     'Host': 'xueqiu.com',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'
# }


header = {

    'path': '/apiv1/content/themes/stream/1005680?type=newest&cursor=1558066610478&limit=20',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'cache-control': 'max-age=0',
    'Connection': 'keep-alive',
    'cookie': '_ga=GA1.2.1121640473.1558350081; device_id=68058d1287ed64009ee8b3ad7483e413; s=bu112pg749; bid=145ffe6154eaf248e7c3f639c59514fa_jvx3494k; aliyungf_tc=AQAAAMG/rlYItAUAs+US2hiFOGNBdYT1; snbim_minify=true; Hm_lvt_1db88642e346389874251b5a1eded6e3=1559557379,1559644535,1560214299,1560312262; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1560473916; xq_token_expire=Sat%20Jul%2013%202019%2008%3A57%3A33%20GMT%2B0800%20(China%20Standard%20Time); xq_is_login=1; u=3405123156; __utma=1.1121640473.1558350081.1560906300.1560906300.1; __utmc=1; __utmz=1.1560906300.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u.sig=HVxEUOB0nWeupmAOxPQNNGo4jk8; xqat=ffb07bf9559fbbeedeae2992048d483c3f992196; xqat.sig=gSZBUh4gEcU1BSyyiKjvQJxoXCs; xq_a_token=ffb07bf9559fbbeedeae2992048d483c3f992196; xq_a_token.sig=ZGDJoapNyc1JKmJFqWllj4Z6MWQ; xq_r_token=f8a4cc77bc23292bf48344215759550ede444340; xq_r_token.sig=ntKBKlrY438FygwINVGxl6tARrI',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}


class Http(object):
    @staticmethod
    def get_content(url='', data=None, timeout=Config.timeout_download_html, extra_header={}):
        u"""
        获取网页内容

        :param url: 需要打开的网页
        :param data: 需要传输的数据, 默认是空
        :param timeout: int 类型的秒数, 打开网页超过这个时间直接退出, 停止等待
        :param extra_header: 字典, 需要添加的 http 头信息
        :return: 打开成功: 返回页面内容, 字符串或二进制数据, 失败: 返回空字符串
        :Exception: 解压缩页面失败时报错
        """
        # 'Cookie': ' xq_a_token=ffa7b19c02a198620f85b3d9d7a93af9939d3eef; bid=140b75475571da90d7d573a14ca9957a_is5c7shi;',

        header.update(extra_header)

        if data:
            data = urllib.urlencode(data)
        request = urllib2.Request(url=url, data=data)
        for key in header:
            request.add_header(key, header[key])

        try:
            response = urllib2.urlopen(request, timeout=timeout)
        except urllib2.HTTPError as error:
            Debug.logger.info(u'网页打开失败')
            Debug.logger.info(u'失败页面: {}'.format(url))
            Debug.logger.info(u'失败代码: {}'.format(error.code))
            Debug.logger.info(u'失败原因: {}'.format(error.reason))
        except urllib2.URLError as error:
            Debug.logger.info(u'网络连接异常')
            Debug.logger.info(u'异常页面: {}'.format(url))
            Debug.logger.info(u'异常原因:{}'.format(error.reason))
        except socket.timeout:
            Debug.logger.info(u'打开网页超时')
            Debug.logger.info(u'超时页面:{}'.format(url))
        except socket.error:
            Debug.logger.info(u'打开网页超时')
            Debug.logger.info(u'超时页面:{}'.format(url))
        except Exception:
            Debug.logger.info(u'未知错误')
            Debug.logger.info(u'错误页面:{}'.format(url))
            Debug.logger.info(u'错误堆栈信息:{}'.format(traceback.format_exc()))
        else:
            content = Http.__unpack(response, url)
            return content
        return ''

    @staticmethod
    def get_json_content(url=''):
        u"""
        获取网页内容
        """

        r = requests.get(url, headers=header)

        return r

    @staticmethod
    def __unpack(response, url=''):
        if not response:
            return ''

        try:
            content = response.read()
        except socket.timeout:
            Debug.logger.info(u'打开网页超时')
            Debug.logger.info(u'超时页面:{}'.format(url))
        except Exception:
            Debug.logger.info(u'未知错误')
            Debug.logger.info(u'报错页面:{}'.format(url))
        else:
            decode = response.info().get(u"Content-Encoding")
            if decode and u"gzip" in decode:
                content = Http.__ungzip(content)
            return content
        return ''

    @staticmethod
    def __ungzip(content):
        try:
            content = zlib.decompress(content, 16 + zlib.MAX_WBITS)
        except zlib.error as error:
            Debug.logger.info(u'解压出错')
            Debug.logger.info(u'错误信息:{}'.format(error))
            return ''
        return content

    @staticmethod
    def set_cookie(account=''):
        if account == 'DontNeed':  # 如果不需要cookie, 一定要主动调用
            return

        def load_cookie(cookieJar, cookie):
            filename = u'./theFileNameIsSoLongThatYouWontKnowWhatIsThat.txt'
            with open(filename, 'w') as f:
                f.write(cookie)
            cookieJar.load(filename)
            os.remove(filename)
            return

        jar = cookielib.LWPCookieJar()
        if account:
            result = DB.cursor.execute(
                "select cookieStr, recordDate from LoginRecord order by recordDate desc where account = `{}`".format(
                    account))
        else:
            result = DB.cursor.execute("select cookieStr, recordDate from LoginRecord order by recordDate desc")

        result = result.fetchone()
        cookie = result[0]
        load_cookie(jar, cookie)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
        urllib2.install_opener(opener)
        return

    @staticmethod
    def make_cookie(name, value, domain):
        cookie = cookielib.Cookie(version=0, name=name, value=value, port=None, port_specified=False, domain=domain,
                                  domain_specified=True, domain_initial_dot=False, path="/", path_specified=True,
                                  secure=False, expires=time.time() + 300000000, discard=False, comment=None,
                                  comment_url=None, rest={})
        return cookie
