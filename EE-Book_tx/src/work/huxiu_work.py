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
from src.lib.parser.huxiu_parser import HuXiuColumnParser, HuXiuArticleParser
import re

import urllib

import sys


class HuXiuWorker(object):
    @staticmethod
    def catch(account_id):
        # 关键就在这里了

        mock_sleep_time = 0.5
        base_sleep_time = 10
        max_sleep_time = 10

        article_url_index_list = []
        #   获取最大页码
        url = 'https://www.huxiu.com/{}'.format(account_id)
        front_page_content = Http.get_content(url)

        # Config.now_id_likeName = account_id
        # Config.save()

        column_info = HuXiuColumnParser(front_page_content).get_column_info()
        column_info[u'column_id'] = account_id
        column_info[u'title'] = account_id

        from src.worker import Worker
        Worker.save_record_list(u'Column', [column_info])

        u_result = urllib.quote(account_id.decode(sys.stdin.encoding).encode('utf8'))
        print account_id
        max_page = 2

        idds = ''
        #
        with open('ReadList.txt', 'r') as read_list:
            read_list = read_list.readlines()
            for line in read_list:
                split_url = line.split('#')[0]
                if split_url.split('/')[-1] == account_id:
                    # Config.now_id_likeName = line.split('#')[1]
                    max_page = int(line.split('#')[-1]) + 1
                    idds = str(line.split('#')[1])
                    print max_page
        # max_page = 1
        #   分析网页内容，存到数据库里


        Debug.logger.info(u"最大页数抓取完毕，共{max_page}页".format(max_page=max_page))
        index_work_set = OrderedDict()
        #   获取每一页中文章的地址的地址
        for raw_front_page_index in range(0, max_page+1):
            # request_url = u'https://www.huxiu.com/search.html?s={}&per_page={}'.format(u_result, raw_front_page_index)
            request_url = u'https://www.huxiu.com/member/{}/article/{}.html'.format(idds,raw_front_page_index)
            # request_url = 'https://www.huxiu.com/member/1872007.html'
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

                soup = BeautifulSoup(request_url_content, "lxml")

                # list_pcyc_l_ = soup.find_all('li')
                list_pcyc_l_ = soup.find_all('div',class_='mob-ctt')
                for tgo_right in list_pcyc_l_:
                    for link in tgo_right.findAll('a'):
                        hre = str(link.get('href'))
                        if hre.startswith('/article/', 0, 10):
                            print u'https://www.huxiu.com{}'.format(link.get('href'))
                            article_url_index_list.append('https://www.huxiu.com{}'.format(link.get('href')))

                del index_work_set[raw_front_page_index]

        article_count = len(article_url_index_list)
        Debug.logger.info(u"文章链接抓取完毕，共{article_count}篇文章待抓取".format(article_count=article_count))

        index_work_set = OrderedDict()
        for article_url_index in article_url_index_list:
            print  'query : '+ article_url_index
            article_db = DB.query_row('select count(*) as article_count from Article where article_id = "{}"'.format(article_url_index))
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

                article_info = HuXiuArticleParser(request_url_content).get_article_info()
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


            #
            # def create_work_set(self, target_url):
            #     if target_url in self.task_complete_set:
            #         return
            #
            #     result = Match.huxiu_author(target_url).group('huxiu_id')
            #     Config.now_id_likeName =  result
            #     Config._save()
            #     u_result =urllib.quote(result.decode(sys.stdin.encoding).encode('utf8'))
            #     print result
            #
            #     range_id = 2
            #
            #     self.task_complete_set.add(target_url)
            #     #
            #     with open('ReadList.txt', 'r') as read_list:
            #         read_list = read_list.readlines()
            #         for line in read_list:
            #             split_url = line.split('#')[0]
            #             if split_url.split('/')[-1] == result :
            #                 # Config.now_id_likeName = line.split('#')[1]
            #                 range_id = int(line.split('#')[-1])+1
            #                 print range_id
            #
            #
            #     # 搜索列表
            #
            #     content_list = []
            #     for indx in range(1, range_id):
            #         url = u'https://www.huxiu.com/search.html?s={}&per_page={}'
            #         uurl = url.format(u_result, indx)
            #
            #         r = Http.get_content(uurl)
            #         if indx == 1:
            #             parser = huxiuAuthorParser(r)
            #             self.question_list += parser.get_extra_info()
            #
            #         soup = BeautifulSoup(r, 'lxml')
            #
            #         list_pcyc_l_ = soup.find_all('li')
            #         for tgo_right in list_pcyc_l_:
            #             for link in tgo_right.findAll('a'):
            #                 hre = str(link.get('href'))
            #                 if hre.startswith('/article/', 0, 10):
            #                     print link.get('href')
            #                     if not content_list.__contains__(u'https://www.huxiu.com{}'.format(link.get('href'))):
            #                         content_list.append(u'https://www.huxiu.com{}'.format(link.get('href')))
            #                         print u'https://www.huxiu.com{}'.format(link.get('href'))
            #     for x in content_list:
            #         self.work_set.add(x)
            #
            #     return
            #
