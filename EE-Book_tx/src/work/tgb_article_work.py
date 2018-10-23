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
from src.lib.parser.tgb_at_parser import TGBArticleParser, TGBColumnParser
import re

import urllib

import sys


class TGBArticleWorker(object):
    @staticmethod
    def catch(account_id):
        # 关键就在这里了

        article_url_index_list = []
        #   获取最大页码
        url = 'http://www.taoguba.com.cn/Article/' + account_id + '/1'
        front_page_content = Http.get_content(url)
        star_page = 1
        max_page = 2
        dom = BeautifulSoup(front_page_content, "lxml")
        list_pcyc_l_ = dom.find_all('div', class_="left t_page01")
        try:
            for tgo_tgo_ in list_pcyc_l_:
                linkl = tgo_tgo_.findAll('a')
                tarUrl = linkl[0].get('href')
                max_page = int(tarUrl.split('/')[3])

        except  IndexError as   e:
            max_page = 1
        column_info = TGBColumnParser(front_page_content).get_column_info()
        # column_info[u'column_id'] = account_id
        # column_info[u'title'] = "股社区"

        # max_page = 3
        from src.worker import Worker
        Worker.save_record_list(u'Column', [column_info])

        from src.worker import Worker
        Worker.save_record_list(u'Column', [column_info])

        Debug.logger.info(u"最大页数抓取完毕，共{max_page}页".format(max_page=max_page))
        index_work_set = OrderedDict()
        # 获取每一页中文章的地址的地址
        for raw_front_page_index in range(star_page, max_page+1):
            request_url = 'http://www.taoguba.com.cn/Article/' + account_id + '/' + str(raw_front_page_index)
            article_url_index_list.append(request_url)

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
                Debug.logger.info(u"开始抓取{countert}号文章，剩余{article_count}篇".format(countert=article_url_index,
                                                                                 article_count=len(index_work_set)))
                request_url_content = Http.get_content(request_url)

                article_info = TGBArticleParser(request_url_content).get_article_info()
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
