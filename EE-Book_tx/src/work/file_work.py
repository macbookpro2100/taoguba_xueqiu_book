# -*- coding: utf-8 -*-


import random
import os
import time
from bs4 import BeautifulSoup

from src.tools.config import Config
from src.tools.db import DB
from src.tools.debug import Debug
from src.tools.http import Http
from src.tools.match import Match
from src.tools.type import Type
from collections import OrderedDict
from src.lib.parser.file_parser import FileArticleParser, FileColumnParser
import re

import urllib

import sys
import chardet
import codecs


def convert_encoding(filename, target_encoding):
    # Backup the origin file.

    # convert file from the source encoding to target encoding
    content = codecs.open(filename, 'r').read()
    source_encoding = chardet.detect(content)['encoding']
    if source_encoding != 'utf-8':
        print source_encoding, filename
        content = content.decode(source_encoding, 'ignore') #.encode(source_encoding)

        content = str(content).replace('charset=gb2312','charset=utf-8',1)
        codecs.open(filename, 'w', encoding=target_encoding).write(content)

class FileWorker(object):

    @staticmethod
    def catch(account_id):
        # 关键就在这里了

        mock_sleep_time = 0.5
        base_sleep_time = 10
        max_sleep_time = 10

        article_url_index_list = []
        #   获取最大页码

        column_info = FileColumnParser('').get_column_info()
        column_info[u'column_id'] = account_id
        column_info[u'title'] = "毛泽东军事文选"

        from src.worker import Worker
        Worker.save_record_list(u'Column', [column_info])
        star_page = 0
        max_page = 1




        from src.worker import Worker
        Worker.save_record_list(u'Column', [column_info])

        Debug.logger.info(u"最大页数抓取完毕，共{max_page}页".format(max_page=max_page))
        index_work_set = OrderedDict()
        #获取每一页中文章的地址的地址

        path = '/Users/ink/Desktop/ht'

        list = os.listdir(path) #列出文件夹下所有的目录与文件
        for i in list:
            # print i

            if str(i).endswith('htm') or str(i).endswith('html'):
                filename = u'/Users/ink/Desktop/ht/{}'.format(i)
                convert_encoding(filename, 'utf-8')
                f = open(filename)
                contents = f.read()
                # print(contents)
                # gb2312 转
                article_info = FileArticleParser(contents).get_article_info()
                if len(article_info) > 0:
                    article_info['article_id'] = i
                    article_info['column_id'] = account_id
                    Worker.save_record_list(u'Article', [article_info])


                f.close()






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
