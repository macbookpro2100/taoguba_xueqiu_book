# -*- coding: utf-8 -*-
import time
from src.tools.db import DB
from src.tools.debug import Debug
from src.tools.XQHttp import Http
# from src.tools.http import Http
from src.tools.match import Match
from src.tools.type import Type
from collections import OrderedDict
from src.lib.parser.xueqiu_parser import XueQiuColumnParser, XueQiuArticleParser
import time


import json


class XueQiuWorker(object):
    @staticmethod
    def catch(account_id):
        # 关键就在这里了
        u"""

        :param target_url: https://xueqiu.com/4065977305
        :return:
        """
        mock_sleep_time = 0.5

        article_url_index_list = []
        #   获取最大页码
        # url = 'http://chuansong.me/account/{}'.format(account_id)
        # front_page_content = Http.get_content(url)
        # max_page = XueQiuWorker.parse_max_page(front_page_content)

        # _url = "http://xueqiu.com/v4/statuses/user_timeline.json?user_id={0}&page={1}&type=2" ''是all  2主贴  5 回复
        _url = "https://xueqiu.com/v4/statuses/user_timeline.json?user_id={0}&page={1}&type="
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

        content_profile = Http.get_content(u'https://xueqiu.com/{}/profile'.format(account_id))

        column_info = XueQiuColumnParser(content_profile).get_column_info()
        column_info[u'column_id'] = account_id

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

                content = Http.get_content(request_url)
                if not content:
                    return
                jdata = json.loads(content)
                articles = jdata['statuses']
                for article in articles:
                    # print article

                    article_info = XueQiuArticleParser(article).get_article_info()
                    if len(article_info) > 0:
                        article_info['article_id'] = article_url_index
                        article_info['column_id'] = account_id
                        Worker.save_record_list(u'Article', [article_info])
                        del index_work_set[article_url_index]

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
