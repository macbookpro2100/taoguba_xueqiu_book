# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from src.lib.wechat_parser.tools.parser_tools import ParserTools
from src.tools.config import Config
from src.tools.match import Match
import datetime

import time

common_used_numerals_tmpy = {'零': '0', '○': '0', '一': '1', '二': '2', '两': '2', '三': '3', '四': '4', '五': '5', '六': '6',
                             '七': '7', '八': '8', '九': '9'}


def chinese2datsty(uchars_chinese):
    for k in common_used_numerals_tmpy:
        x = common_used_numerals_tmpy[k]
        uchars_chinese = uchars_chinese.replace(k, x, 4)
    return uchars_chinese


class FileColumnParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'html.parser')

    def get_column_info(self):
        data = {}

        data['title'] = ""
        data['article_count'] = 0
        data['follower_count'] = 0
        data['description'] = ''
        data['image_url'] = ''

        return data


class FileArticleParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'lxml')

    def get_article_info(self):
        data = {}
        try:

            try:
                title_tationl = self.dom.find_all('p', align="center")
                # print  u"标题 {}".format(span_dom.text.strip()),
                resultstr = title_tationl[0].text
                data['title'] = resultstr

                ttd = title_tationl[1].text
                td = (str(ttd).split('（')[-1]).split('）')[0]
                # date_time = datetime.datetime.strptime(td, '%Y年%m月%d日')
                print td
                ye = td.split('年')[0]
                mo = (td.split('年')[-1]).split('月')[0]
                da = (td.split('月')[-1]).split('日')[0]

                yey = chinese2datsty(ye)

                print u'{}年{}月{}'.format(yey,mo,da)
                data['updated_time'] = u'{}年{}月{}'.format(yey,mo,da)

            except IndexError:
                data['title'] = Match.replace_specile_chars(self.dom.title)
                data['updated_time'] = ''
            data['title'] = str(data['title']).strip()

            article_body = ""

            content = self.dom.find_all('p')
            for ii in range(2, len(content)):
                x = content[ii]
                # print x
                xxt = u'<p>{}</p>'.format(x.text)
                article_body += str(xxt)

            data['content'] = str(article_body)

            data['voteup_count'] = ""
            data['comment_count'] = ""

            data['image_url'] = ''

            data['author_id'] = 'meng-qing-xue-81'

            data['author_name'] = '   '
            data['author_headline'] = ''
            data['author_avatar_url'] = 'https://pic4.zhimg.com/v2-38a89e42b40baa7d26d99cab9a451623_xl.jpg'
            data['author_gender'] = '0'
        except Exception as e:
            print e.message
            return []

        return data
