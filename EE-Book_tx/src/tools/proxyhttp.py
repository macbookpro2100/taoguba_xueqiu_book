# -*- coding: utf-8 -*-
"""
Created on Sat Mar 03 19:06:18 2018
@author: Administrator
"""

import urllib2
import re
import requests
import time
from threading import Thread
from threading import Lock
from Queue import Queue




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


        my_headers = [
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0""Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
            "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"]
        # header = {'User-Agent': random.choice(my_headers)}
        header = {
            'User-Agent': random.choice(my_headers),
            'Referer': url
        }

        if str(url).startswith("http://img.chuansong.me"):
            header = {
                'User-Agent': random.choice(my_headers),
                'Host': "img.chuansong.me",

            }


        # header = {
        #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        #     'Accept-Encoding': ' gzip, deflate',
        #     'Accept-Language': ' zh-CN,zh;q=0.9',
        #     'Cache-Control': ' max-age=0',
        #     'Connection': ' keep-alive',
        #     'Cookie': 'traid=4196e041984e47be948ffa522a9ade00; Hm_lvt_723459747aa85ac30c7586a117fc73d9=1534476689,1535114936,1535379292,1535618269; Hm_lpvt_723459747aa85ac30c7586a117fc73d9=1535623774',
        #     'Host':'www.jintiankansha.me' ,
        #     'If-None-Match':' W/"acd4d87df75374da21c7f22810e8db90e2fe3009"',
        #     'Referer': url,
        #     'Upgrade-Insecure-Requests': ' 1',
        #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        # }


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



#获取 可用代理
#从西刺抓下来的所有代理ip
all_find_list=[]
#将所有抓到的代理压入队列，四个线程可以从队列中获取代理ip
gaoni_queue=Queue()
#能够成功连接的代理ip
success_list=[]

lock=Lock()

def get_proxy(checking_ip):
    #根据得到的代理ip，设置proxy的格式
    proxy_ip = 'http://' + checking_ip
    proxy_ips = 'https://' + checking_ip
    proxy = {'https': proxy_ips, 'http': proxy_ip}
    return proxy

def checking_ip():
    global gaoni_queue
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    while 1:
        #若从队列1秒内无法获得代理ip，说明所有代理均已检测完成，抛出Empty异常
        try:
            checking_ip = gaoni_queue.get(True,1)
        except:
            gaoni_queue.task_done()
            break

        proxy=get_proxy(checking_ip)
        url = 'http://chuansong.me/'
        #使用上面的url，测试代理ip是否能够链接
        try:
            page = requests.get(url, headers=headers, proxies=proxy)
        except:
            lock.acquire()
            print checking_ip,'失败'.decode('utf-8')
            lock.release()
        else:
            lock.acquire()
            print checking_ip,'成功'.decode('utf-8')
            success_list.append(checking_ip)
            lock.release()


def get_all():
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    global all_find_list
    for i in range(1,2):
        #从xici网站的高匿页面获取ip
        url='http://www.xicidaili.com/nn/%d'%i
        r = requests.get(url,headers=headers)
        data=r.text
        #抓取所需数据的正则表达式
        p=r'<td>(.*?)</td>\s+<td>(.*?)</td>\s+<td>\s+(.*?)\s+</td>\s+<td class="country">(.*?)</td>'
        find_list=re.findall(p,data)
        all_find_list+=find_list
    #将ip地址与端口组成规定格式
    for row in all_find_list:
        ip=row[0]+':'+row[1]
        gaoni_queue.put(ip)



if __name__=='__main__':
    get_all()
    print gaoni_queue.qsize()
    thread_1=Thread(target=checking_ip)
    thread_2=Thread(target=checking_ip)
    thread_3=Thread(target=checking_ip)
    thread_4=Thread(target=checking_ip)
    thread_1.start()
    thread_2.start()
    thread_3.start()
    thread_4.start()
    thread_1.join()
    thread_2.join()
    thread_3.join()
    thread_4.join()
    f=open("ip.txt","w")
    for row in success_list:
        f.write(row+'\n')
    f.close()
