#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time
import json
import requests
import urllib

from bs4 import BeautifulSoup

from ..tools.XQHttp import Http
from ..tools.match import Match

from ..tools.controler import Control
from ..tools.db import DB
from ..tools.debug import Debug

from ..lib.xueqiu_parser.xueqiu_parser import XueQiuParser
from ..lib.xueqiu_parser.xueqiu_artic_parser import XueQiuArticleParser

from ..lib.parser_tools import ParserTools

__all__ = [
    "xueqiuAuthorWorker",
]


class xueqiuAuthorWorker(object):
    def __init__(self, task_list):
        self.task_set = set(task_list)
        self.task_complete_set = set()
        self.work_set = set()  # 待抓取网址池
        self.work_complete_set = set()  # 已完成网址池
        self.content_list = []  # 用于存放已抓取的内容

        self.answer_list = []
        self.question_list = []

        self.info_list = []
        self.extra_index_list = []
        self.info_url_set = self.task_set.copy()
        self.info_url_complete_set = set()

        # 添加扩展属性
        self.add_property()

    def add_property(self):

        return

    @staticmethod
    def parse_max_page(content):
        max_page = 1
        try:
            floor = content.index('">下一页</a></span>')
            floor = content.rfind('</a>', 0, floor)
            cell = content.rfind('>', 0, floor)
            max_page = int(content[cell + 1:floor])
            Debug.logger.info(u'答案列表共计{}页'.format(max_page))
        except:
            Debug.logger.info(u'答案列表共计1页')
        finally:
            return max_page

    def clear_index(self):
        u"""
        用于在collection/topic中清除原有缓存
        """
        return

    def save(self):
        self.clear_index()
        save_config = self.create_save_config()
        for key in save_config:
            for item in save_config[key]:
                if item:
                    DB.save(item, key)
        DB.commit()
        return

    def start(self):
        self.start_catch_info()
        self.start_create_work_list()
        self.start_worker()
        self.save()
        return

    def clear_work_set(self):
        self.work_set = set()
        return

    def start_create_work_list(self):
        self.clear_work_set()
        argv = {
            'function': self.create_work_set,
            'iterable': self.task_set,
        }
        Control.control_center(argv, self.task_set)
        return

    def worker(self, target_url):
        if target_url in self.work_complete_set:
            # 自动跳过已抓取成功的网址
            return
        Debug.logger.info(u'开始抓取 {} 的内容'.format(target_url))

        content = Http.get_content(target_url)
        if not content:
            return
        jdata = json.loads(content)
        articles = jdata['statuses']
        for article in articles:

            self.content_list.append(article)
        Debug.logger.debug(u' {} 的内容抓取完成'.format(target_url))
        # 延时
        time.sleep(3)
        self.work_complete_set.add(target_url)
        return

    def start_worker(self):
        u"""
        work_set是所有的需要抓取的页面(单篇的文章)
        :return:
        """
        work_set_list = list(self.work_set)
        work_set_list.sort()
        argv = {
            'function': self.worker,  # 所有待存入数据库中的数据都应当是list
            'iterable': work_set_list,
        }
        Control.control_center(argv, self.work_set)
        Debug.logger.info(u"所有内容抓取完毕，开始对页面进行解析")
        for i, content in enumerate(self.content_list):
            Debug.print_in_single_line(u"正在解析第{}/{}张页面".format(i, self.content_list.__len__()))
            self.parse_content(json.dumps(content))
        Debug.logger.info(u"网页内容解析完毕")
        return

    def catch_info(self, target_url):
        # if target_url in self.info_url_complete_set:
        #     return
        # content = Http.get_content(target_url)
        # if not content:
        #     return
        # self.info_url_complete_set.add(target_url)
        # parser = XueQiuParser(content)
        # self.info_list.append(parser.get_extra_info())
        return

    def start_catch_info(self):
        argv = {
            'function': self.catch_info,
            'iterable': list(self.info_url_set),
        }
        Control.control_center(argv, self.info_url_set)
        return

    def create_save_config(self):
        config = {'xueqiu_article': self.answer_list, 'xueqiu_info': self.question_list}
        return config

    def parse_content(self, content):

        parser = XueQiuArticleParser(str(content))
        self.answer_list += parser.get_answer_list()

    def create_work_set(self, target_url):
        u"""

        :param target_url: https://xueqiu.com/4065977305
        :return:
        """
        if target_url in self.task_complete_set:
            return
        first_page_of_author_id = Match.xueqiu_author(target_url).group("xueqiu_author_id")
        print first_page_of_author_id

        # _url = "http://xueqiu.com/v4/statuses/user_timeline.json?user_id={0}&page={1}&type=2" 2主贴  5 回复
        _url = "https://xueqiu.com/v4/statuses/user_timeline.json?user_id={0}&page={1}&type="
        first = _url.format(first_page_of_author_id, 1)
        r = Http.get_json_content(first)
        try:
            jdata = json.loads(r.text, encoding='utf-8')
            maxpage = jdata['maxPage'] + 1
            # todo debug max
            # maxpage = 2
            for page in xrange(1, maxpage):
                url = _url.format(first_page_of_author_id, page)  # page from 1
                self.work_set.add(url)
        except KeyError as   e:
            print  '打开失败 >>>>>>> Cookie'

        # self.task_complete_set.add(target_url)
        # 取作者信息

        content_profile = Http.get_content(u'https://xueqiu.com/{}/profile'.format(first_page_of_author_id))
        parser = XueQiuParser(content_profile)
        self.question_list += parser.get_extra_info()

        return
