# -*- coding: utf-8 -*-
import time
from src.tools.db import DB
from src.tools.debug import Debug
from src.tools.XQHttp import Http
# from src.tools.http import Http
from src.tools.match import Match
from src.tools.type import Type
from collections import OrderedDict
from src.lib.parser.wallstreetcn_parser import WallStreetcnArticleParser
import time

import json


def resuorcecatch(account_id, strtT):
    _url = "https://api.wallstreetcn.com/apiv1/content/themes/stream/{0}?type=newest&cursor={1}&limit=20"

    f = open(u'TGB_List页面.txt', 'a')

    first = _url.format(account_id, strtT)
    r = Http.get_json_content(first)

    try:
        jdata = json.loads(r.content, encoding='utf-8')
        max_page = jdata['data']['next_cursor']

        articles = jdata['data']['items']

        print max_page

        for article in articles:
            if article['resource'].has_key('uri'):
               taffy = article['resource']['uri']
               # title=  article['resource']['title']
               if str(taffy).__contains__('articles'):
                   wt = u'{}\n'.format(taffy)
                   f.write(wt)
                   print taffy



        # for article in articles:
        #     article_info = WallStreetcnArticleParser(article).get_article_info()
        #     if len(article_info) > 0:
        #         article_info['column_id'] = account_id
        #         from src.worker import Worker
        #         Worker.save_record_list(u'Article', [article_info])
        #
        #         Debug.logger.debug(u'第 {} 的内容抓取完成'.format(max_page))

        resuorcecatch(account_id, max_page)

        return max_page


    except KeyError as   e:
        print e
        print  '打开失败 >>>>>>> Cookie'


class WallStreetcnWorker(object):
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

        column_info = {}
        column_info[u'column_id'] = account_id
        column_info[u'title'] = ""
        column_info['article_count'] = 0
        column_info['follower_count'] = 0
        column_info['description'] = ''
        column_info['image_url'] = ''

        from src.worker import Worker
        Worker.save_record_list(u'Column', [column_info])

        strtT = '1558513651020'

        # https://api.wallstreetcn.com/apiv1/content/themes/stream/1005680?type=newest&cursor=1558066610478&limit=20



        max_page = 2
        index_work_set = OrderedDict()
        #   获取每一页中文章的地址的地址
        for raw_front_page_index in range(1, max_page):
            resuorcecatch(account_id, strtT)
