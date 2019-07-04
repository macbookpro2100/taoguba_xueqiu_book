# -*- coding: utf-8 -*-


import random

import time
from bs4 import BeautifulSoup

from src.tools.config import Config
from src.tools.db import DB
from src.tools.debug import Debug
from src.tools.http import Http
from src.tools.match import Match
from src.tools.type import Type
from collections import OrderedDict
from src.lib.parser.wxhttp_parser import WeiXinArticleParser, WeiXinColumnParser ,WallStreetArticleParser

from src.lib.parser.todo2_parser import Todo2ArticleParser, Todo2ColumnParser
from src.lib.parser.huxiu_parser import HuXiuArticleParser
import re

import urllib

import sys


class WeiXinWorker(object):
    @staticmethod
    def catch(account_id):
        # 关键就在这里了

        mock_sleep_time = 0.5
        base_sleep_time = 1
        max_sleep_time = 1

        article_url_index_list = []
        #   获取最大页码

        column_info = WeiXinColumnParser('').get_column_info()
        column_info[u'column_id'] = account_id
        column_info[u'title'] = account_id
        column_info[u'image_url'] = 'https://wpimg.wallstcn.com/3598b719-ab0d-4be7-bc09-30c3ae29a3cc.jpg?imageView2/1/w/240/h/240'
        max_page = 1
        # with open('ReadList.txt', 'r') as read_list:
        #     read_list = read_list.readlines()
        #     for line in read_list:
        #         split_url = line.split('#')[0]
        #         if str(split_url).__contains__(account_id):
        #             # Config.now_id_likeName = line.split('#')[1]
        #             max_page = int(line.split('#')[-1]) + 1
        #             column_info[u'title'] = str(line.split('#')[1])
        #
        #             # max_page = 1
        #             print max_page



        from src.worker import Worker
        Worker.save_record_list(u'Column', [column_info])

        Debug.logger.info(u"最大页数抓取完毕，共{max_page}页".format(max_page=max_page))


        # article_url_index_list.append('https://mp.weixin.qq.com/s?__biz=MjM5MjczNDc0Mw==&mid=2650847984&idx=2&sn=b7b111e5964d2f2fb568ba0d419e3edf&chksm=bd55d1888a22589e2f3bab0613b346427079efc6b82fac869d4f78244a500c3e5cc8cb8402ed&scene=21#wechat_redirect')
        # article_url_index_list.append('https://mp.weixin.qq.com/s/yj1BT3jWyxLjlEnzz0vEtQ')

        with open('/Users/0/Desktop/list.txt', 'r') as read_list:
            read_list = read_list.readlines()
            for line in read_list:
                article_url_index_list.append(str(line).strip('\n'))

        article_count = len(article_url_index_list)
        Debug.logger.info(u"文章链接抓取完毕，共{article_count}篇文章待抓取".format(article_count=article_count))

        index_work_set = OrderedDict()
        for article_url_index in article_url_index_list:
            print  'query : ' + article_url_index
            article_db = DB.query_row(
                    'select count(*) as article_count from Article where article_id = "{}"'.format(article_url_index))
            if article_db['article_count'] > 0:
                continue

            request_url = article_url_index

            index_work_set[article_url_index] = request_url

        re_catch_counter = 0
        while len(index_work_set) > 0 and re_catch_counter <= 20:
            re_catch_counter += 1
            for article_url_index in index_work_set:
                request_url = index_work_set[article_url_index]
                Debug.logger.info(u"开始抓取  {countert} 号文章，剩余{article_count}篇".format(countert=article_url_index,
                                                                                    article_count=len(index_work_set)))
                request_url_content = Http.get_content(request_url)
                time.sleep(mock_sleep_time)
                if len(request_url_content) == 0:
                    random_sleep_time = base_sleep_time + random.randint(0, max_sleep_time) / 100.0
                    Debug.logger.info(u"随机休眠{}秒".format(random_sleep_time))
                    time.sleep(random_sleep_time)
                    continue
                #article_info = Todo2ArticleParser(request_url_content).get_article_info()
                # article_info = HuXiuArticleParser(request_url_content).get_article_info()
                article_info = WeiXinArticleParser(request_url_content).get_article_info()
                # article_info = WallStreetArticleParser(request_url_content).get_article_info()
                if len(article_info) > 0:
                    article_info['article_id'] = article_url_index
                    article_info['column_id'] = account_id
                    Worker.save_record_list(u'Article', [article_info])
                del index_work_set[article_url_index]
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

    @staticmethod
    def parse_max_page(content):
        max_page = 1
        try:
            floor = content.index('style="float: right">下一页</a>')
            floor = content.rfind('</a>', 0, floor)
            cell = content.rfind('>', 0, floor)
            max_page = int(content[cell + 1:floor])
            Debug.logger.info(u'答案列表共计{}页'.format(max_page))
        except:
            Debug.logger.info(u'答案列表共计1页')
        finally:
            return max_page
