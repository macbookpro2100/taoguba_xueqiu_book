# -*- coding: utf-8 -*-


import random

import time

import datetime
from bs4 import BeautifulSoup

from src.tools.config import Config
from src.tools.db import DB
from src.tools.debug import Debug
from src.tools.http import Http
from src.tools.match import Match
from src.tools.type import Type
from collections import OrderedDict
from src.lib.parser.jianwks_parser import JinWanKanSaArticleParser, JinWanKanSaColumnParser,JinWanKanSaEmptColumnParser
import re

import urllib

import sys


class JinWanKanSaTodayWorker(object):
    @staticmethod
    def catch(account_id):
        # 关键就在这里了

        mock_sleep_time = 0.5
        base_sleep_time = 1
        max_sleep_time = 1

        article_url_index_list = []
        #   获取最大页码

        url = 'http://www.jintiankansha.me/tag/{}?page=1'.format(account_id)

        column_info = JinWanKanSaEmptColumnParser('').get_column_info()

        column_info[u'column_id'] = account_id
        dt = datetime.datetime.now()
        column_info[u'title'] = u"AI_{}".format(dt.strftime("%Y-%m-%d"))
        max_page = 1

        typeToTry = 'tag'

        with open('ReadList.txt', 'r') as read_list:
            read_list = read_list.readlines()
            for line in read_list:
                split_url = line.split('#')[0]
                if split_url.split('/')[-1] == account_id:
                    dt = datetime.datetime.now()
                    column_info[u'title'] = u"{}_{}".format(line.split('#')[1], dt.strftime("%Y-%m-%d"))

                    max_page = int(line.split('#')[2])

                    typeToTry = str(int(line.split('#')[-1])).strip('\n')


        from src.worker import Worker
        Worker.save_record_list(u'Column', [column_info])

        Debug.logger.info(u"最大页数抓取完毕，共{max_page}页".format(max_page=max_page))
        index_work_set = OrderedDict()
        #   获取每一页中文章的地址的地址
        for raw_front_page_index in range(0, max_page+1):
            # request_url = u'http://www.jintiankansha.me/column/{}?page={}'.format(account_id, raw_front_page_index)
            request_url = u'http://www.jintiankansha.me/{}/{}?page={}'.format(typeToTry,account_id, raw_front_page_index)
            print request_url
            index_work_set[raw_front_page_index] = request_url

        re_catch_counter = 0
        catch_counter = 0
        while len(index_work_set) > 0 and re_catch_counter <= 20:
            re_catch_counter += 1
            for raw_front_page_index in index_work_set:
                catch_counter += 1
                Debug.logger.info(u'第『{}』遍抓取数据'.format(re_catch_counter))
                request_url = index_work_set[raw_front_page_index]
                Debug.logger.info(
                        u"开始抓取第{raw_front_page_index}页中的文章链接，剩余{max_page}页".format(
                                raw_front_page_index=raw_front_page_index, max_page=len(index_work_set)))
                request_url_content = Http.get_content(request_url)

                soup = BeautifulSoup(request_url_content, 'html.parser')
                list_p_list = soup.find_all('span', class_="item_title")

                for tgo_right in list_p_list:
                    for link in tgo_right.findAll('a'):
                        ttt = str(link.get('href'))
                        print ttt
                        if not (ttt is None):
                            article_url_index_list.append(ttt)




                del index_work_set[raw_front_page_index]

        # article_url_index_list.append('http://www.jintiankansha.me/t/u8MygoqKI8')

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
                article_info = JinWanKanSaArticleParser(request_url_content).get_article_info()
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
