# -*- coding: utf-8 -*-


import time

from bs4 import BeautifulSoup

from src.lib.wechat_parser.tools.parser_tools import ParserTools
from src.tools.db import DB
from src.tools.debug import Debug
from src.tools.http import Http
from src.tools.match import Match
from src.tools.type import Type
from collections import OrderedDict
from src.lib.parser.sina_parser import SinaColumnParser, SinaArticleParser


class SinaWorker(object):
    @staticmethod
    def catch(account_id):
        # 关键就在这里了

        mock_sleep_time = 0.5

        article_url_index_list = []
        #   获取最大页码
        url = 'http://blog.sina.com.cn/s/articlelist_{}_11_1.html'.format(account_id)
        front_page_content = Http.get_content(url)
        article_num = SinaWorker.parse_max_page(front_page_content)

        href_profile = 'http://blog.sina.com.cn/s/profile_{}.html'.format(account_id)
        content_profile = Http.get_content(href_profile)

        column_info = SinaColumnParser(content_profile).get_column_info()
        column_info[u'column_id'] = account_id

        from src.worker import Worker
        Worker.save_record_list(u'Column', [column_info])


        index_work_set = OrderedDict()
        #   获取每一页中文章的地址的地址


        if article_num % 50 != 0:
            page_num = article_num / 50 + 1  # 50 href on 1 page
        else:
            page_num = article_num / 50
        Debug.logger.info(u"最大页数抓取完毕，共{max_page}页".format(max_page=page_num))
        index_work_set = OrderedDict()
        for page in range(page_num):
            url = 'http://blog.sina.com.cn/s/articlelist_{}_11_{}.html'.format(account_id, page + 1)
            content_article_list = Http.get_content(url)

            soup = BeautifulSoup(content_article_list, "lxml")

            article_list = soup.select('span.atc_title a')
            for item in range(len(article_list)):
                article_title = ParserTools.get_attr(article_list[item], 'href')

                index_work_set[item] = article_title

        re_catch_counter = 0
        while len(index_work_set) > 0 and re_catch_counter <= 20:
            re_catch_counter += 1
            for article_url_index in index_work_set:
                request_url = index_work_set[article_url_index]
                Debug.logger.info(u"开始抓取{countert}号文章，剩余{article_count}篇".format(countert=article_url_index,
                                                                                 article_count=len(index_work_set)))
                request_url_content = Http.get_content(request_url)
                time.sleep(mock_sleep_time)
                if len(request_url_content) == 0:
                    Debug.logger.info(u"休眠{}秒".format(mock_sleep_time))
                    time.sleep(mock_sleep_time)
                    continue

                article_info = SinaArticleParser(request_url_content).get_article_info()
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
        u"""

        :param content: 博客目录的content
        :return: 博文总数量
        """
        soup = BeautifulSoup(content, "lxml")
        article_num = soup.select('div.SG_connHead span em')
        article_num = article_num[0].get_text()
        article_num = article_num[1:-1]  # 去掉前后两个括号
        return int(article_num)
