# -*- coding: utf-8 -*-
import os
import traceback
import urllib2
import urllib
import socket  # 用于捕获超时错误
import zlib
import cookielib  # 用于生成cookie
import time

from src.tools.config import Config
from src.tools.db import DB
from src.tools.debug import Debug
import random

class Http(object):
    @staticmethod
    def get_content(url='', data=None, timeout=Config.timeout_download_html, extra_header={}):
        u"""获取网页内容

        获取网页内容, 打开网页超过设定的超时时间则报错

        参数:
            url         一个字符串,待打开的网址
            extraHeader 一个简单字典,需要添加的http头信息
            data        需传输的数据,默认为空
            timeout     int格式的秒数，打开网页超过这个时间将直接退出，停止等待
        返回:
            pageContent 打开成功时返回页面内容，字符串或二进制数据|失败则返回空字符串
        报错:
            IOError     当解压缩页面失败时报错
        """
        # UA还是得要啊。。。
        # 没UA知乎分分钟只返回给你首页看- -



        if not str(url).startswith('http'):
            if str(url).startswith('wp-content'):
                url = u"http://www.199it.com/{}".format(url)


        my_headers = [
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0""Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
            "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"]

        if str(url).startswith("https://upload-images"):
            header = {
                'User-Agent': random.choice(my_headers),
                'Host': "upload-images.jianshu.io",

            }
        elif str(url).__contains__('img.3ygk.com'):
            header = {
                'User-Agent': random.choice(my_headers),
                'Host': "img.3ygk.com",

            }
        elif str(url).__contains__('img2.jintiankansha.me'):
            header = {
                'User-Agent': random.choice(my_headers),
                'Host': "img2.jintiankansha.me",
                'Upgrade-Insecure-Requests':'1',
                'Cache-Control':'max-age=0',
                'Connection':'keep-alive',
                'Cookie':'traid=4196e041984e47be948ffa522a9ade00; Hm_lvt_723459747aa85ac30c7586a117fc73d9=1535114936,1535379292,1535618269,1535696406; Hm_lpvt_723459747aa85ac30c7586a117fc73d9=1535696406',
            }

        elif str(url).__contains__('mmbiz.qpic.cn'):
            header = {
                'User-Agent': random.choice(my_headers),
                'Host': "mmbiz.qpic.cn",

            }
        elif str(url).__contains__('gzm.ai800.top'):
            header = {
                'User-Agent': random.choice(my_headers),
                'Host': "gzm.ai800.top",
                'If-None-Match': url
            }
        else :
            header = {
                'User-Agent': random.choice(my_headers),
                'Referer': url
            }



        if data:
            data = urllib.urlencode(data)
        request = urllib2.Request(url=url, data=data)
        for key in header:
            request.add_header(key, header[key])

        try:
            response = urllib2.urlopen(request, timeout=timeout)
        except urllib2.HTTPError as error:
            Debug.logger.info(u'网页打开失败')
            Debug.logger.info(u'失败页面:{}'.format(url))
            Debug.logger.info(u'失败代码:{}'.format(error.code))
            Debug.logger.info(u'失败原因:{}'.format(error.reason))
        except urllib2.URLError as error:
            Debug.logger.info(u'网络连接异常')
            Debug.logger.info(u'异常页面:{}'.format(url))
            Debug.logger.info(u'异常原因:{}'.format(error.reason))
        except socket.timeout as error:
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
    def __unpack(response, url=''):
        if not response:
            return ''

        try:
            content = response.read()
        except socket.timeout as error:
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
