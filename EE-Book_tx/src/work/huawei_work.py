# -*- coding: utf-8 -*-


import random

import time


from src.tools.db import DB
from src.tools.debug import Debug
from src.tools.http import Http
from src.tools.match import Match
from src.tools.type import Type
from collections import OrderedDict
from src.lib.parser.huawei_parser import HuaWeiColumnParser, HuaWeiArticleParser

class HuaWeiWorker(object):
    @staticmethod
    def catch(account_id):
        # 关键就在这里了

        mock_sleep_time = 0.5
        base_sleep_time = 10
        max_sleep_time = 10

        article_url_index_list =[]
        #   获取最大页码
        url = 'http://chuansong.me/account/{}'.format(account_id)
        front_page_content = Http.get_content(url)
        max_page =HuaWeiWorker.parse_max_page(front_page_content)
        if max_page > 200:
            max_page =200
        # max_page = 1
        #   分析网页内容，存到数据库里
        column_info = HuaWeiColumnParser(front_page_content).get_column_info()
        column_info[u'column_id'] = account_id

        from src.worker import Worker
        Worker.save_record_list(u'Column', [column_info])

        Debug.logger.info(u"最大页数抓取完毕，共{max_page}页".format(max_page=max_page))
        index_work_set = OrderedDict()
        #   获取每一页中文章的地址的地址
        for raw_front_page_index in range(0, max_page):
            front_page_index = raw_front_page_index * 12
            request_url = url + '?start={}'.format(front_page_index)
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
                        u"开始抓取第{raw_front_page_index}页中的文章链接，剩余{max_page}页".format(raw_front_page_index=raw_front_page_index, max_page=len(index_work_set)))
                request_url_content = Http.get_content(request_url)
                time.sleep(mock_sleep_time)
                if len(request_url_content) == 0 or catch_counter % 5 == 0:
                    random_sleep_time = base_sleep_time + random.randint(0, max_sleep_time) / 100.0
                    Debug.logger.info(u"随机休眠{}秒".format(random_sleep_time))
                    time.sleep(random_sleep_time)
                    continue

                article_url_index_list += Match.wechat_article_index(content=request_url_content)
                del index_work_set[raw_front_page_index]

        article_count = len(article_url_index_list)
        Debug.logger.info(u"文章链接抓取完毕，共{article_count}篇文章待抓取".format(article_count=article_count))

        index_work_set = OrderedDict()
        for article_url_index in article_url_index_list:
            article_db = DB.query_row('select count(*) as article_count from Article where article_id = {}'.format(article_url_index))
            if article_db['article_count'] > 0:
                continue

            request_url = 'http://chuansong.me/n/{}'.format(article_url_index)
            index_work_set[article_url_index] = request_url

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
                    random_sleep_time = base_sleep_time + random.randint(0, max_sleep_time) / 100.0
                    Debug.logger.info(u"随机休眠{}秒".format(random_sleep_time))
                    time.sleep(random_sleep_time)
                    continue

                article_info = HuaWeiArticleParser(request_url_content).get_article_info()
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