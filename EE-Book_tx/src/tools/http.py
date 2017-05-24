# -*- coding: utf-8 -*-

import os
import traceback
import urllib2
import urllib
import socket  # 用于捕获超时错误
import zlib
import cookielib  # 用于生成cookie
import time

from config import Config
from db import DB
from debug import Debug


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
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
        }
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
        if account == 'DontNeed':           # 如果不需要cookie, 一定要主动调用
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
