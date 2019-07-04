# -*- coding: utf-8 -*-
import time

import datetime

from src.tools.db import DB
from src.tools.debug import Debug
from src.tools.XQHttp import Http
# from src.tools.http import Http
from src.tools.match import Match
from src.tools.type import Type
from collections import OrderedDict
from src.lib.parser.xueqiu_parser import XueQiuColumnParser,XueQiuArticleParser
import time

import json
import random


class XueQiuCWorker(object):
    @staticmethod
    def catch(account_id):
        # 关键就在这里了
        u"""

        :param target_url: https://xueqiu.com/4065977305
        :return:
        """
        mock_sleep_time = 0.5
        base_sleep_time = 5
        max_sleep_time = 30

        article_url_index_list = []

               #https://xueqiu.com/statuses/search.json?count=10&comment=0&symbol=SZ000333&hl=0&source=all&sort=&page=1&q=

        _url = "https://xueqiu.com/statuses/search.json?count=10&comment=0&symbol={0}&hl=0&source=all&sort=alpha&page={1}&q="

        # 搜索 霍华德·马克斯
        # _url = "https://xueqiu.com/statuses/search.json?sort=relevance&source=all&q={0}&count=10&page={1}"

        first = _url.format(account_id, 1)
        r = Http.get_json_content(first)
        max_page = 1
        try:
            jdata = json.loads(r.text, encoding='utf-8')
            max_page = jdata['maxPage'] + 1
        except KeyError as   e:
            print  '打开失败 >>>>>>> Cookie'
        # max_page = 1
        #   分析网页内容，存到数据库里
        #   需要验证码

        max_page = 1
        # print max_page


        column_info = XueQiuColumnParser('').get_column_info()
        column_info[u'column_id'] = account_id
        column_info[u'title'] = ""

        with open('ReadList.txt', 'r') as read_list:
            read_list = read_list.readlines()
            for line in read_list:
                split_url = line.split('#')[0]
                if split_url.split('/')[-1] == account_id:

                    dt = datetime.datetime.now()
                    tit = line.split('#')[1]
                    column_info[u'title'] = u"{}_{}".format(tit, dt.strftime("%Y-%m-%d"))

                    column_info[u'image_url'] = str(line.split('#')[2]).strip('\n')

        from src.worker import Worker
        Worker.save_record_list(u'Column', [column_info])

        Debug.logger.info(u"最大页数抓取完毕，共{max_page}页".format(max_page=max_page))

        #

        index_work_set = OrderedDict()
        #   获取每一页中文章的地址的地址
        for raw_front_page_index in range(1, max_page):
            request_url = _url.format(account_id, raw_front_page_index)
            index_work_set[raw_front_page_index] = request_url

        re_catch_counter = 0
        while len(index_work_set) > 0 and re_catch_counter <= 20:
            re_catch_counter += 1
            for article_url_index in index_work_set:
                request_url = index_work_set[article_url_index]
                Debug.logger.info(u"开始抓取{countert}号文章，剩余{article_count}篇".format(countert=article_url_index,
                                                                                 article_count=len(index_work_set)))


                print  request_url
                content = Http.get_content(request_url)
                if not content:

                    random_sleep_time = base_sleep_time + random.randint(2, max_sleep_time) / 10.0
                    Debug.logger.info(u"随机休眠{}秒".format(random_sleep_time))
                    time.sleep(random_sleep_time)
                    continue


                    # {"error_description":"您的请求过于频繁，请稍后再试","error_uri":"/statuses/search.json","error_code":"22612"}


                jdata = json.loads(content)


                if jdata.has_key('error_code'):
                    random_sleep_time = base_sleep_time + random.randint(3, max_sleep_time) / 10.0
                    Debug.logger.info(u"error_description {}秒".format(jdata['error_description']))
                    time.sleep(random_sleep_time)
                    continue

                articles = jdata['list']

                for article in articles:
                    # print article

                    article_info = XueQiuArticleParser(article).get_article_info()
                    if len(article_info) > 0:
                        article_info['column_id'] = account_id
                        Worker.save_record_list(u'Article', [article_info])
                del index_work_set[article_url_index]

                random_sleep_time = 1 + random.randint(3, max_sleep_time) / 10.0
                Debug.logger.info(u"随机休眠{}秒".format(random_sleep_time))
                time.sleep(random_sleep_time)

                Debug.logger.debug(u' {} 的内容抓取完成'.format(request_url))

        return

    @staticmethod
    def format_column(raw_column):
        u"""

        :param raw_column: src.lib.oauth.zhihu_oauth.zhcls.Column
        :return:
        """
        column_key_list = [
            u'title',
            u'article_count',
            u'description',
            u'follower_count',
            u'image_url',
        ]
        column_info = {}
        for key in column_key_list:
            column_info[key] = getattr(raw_column, key, u'')

        column_info[u'column_id'] = raw_column._id

        return column_info
