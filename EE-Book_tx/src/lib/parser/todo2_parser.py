# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from src.lib.wechat_parser.tools.parser_tools import ParserTools
from src.tools.config import Config
from src.tools.match import Match
import datetime

import time

class Todo2ColumnParser(ParserTools):
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


class Todo2ArticleParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'lxml')

    def get_article_info(self):
        data = {}
        try:

            try:
                title_tationl  = self.dom.select('div.article-header header')[0]
                # print  u"标题 {}".format(span_dom.text.strip()),


                resultstr = title_tationl.text

                print resultstr


                if resultstr.__contains__('/'):
                    resultstr = Match.replace_specile_chars(resultstr)
                data['title'] = resultstr

                data['title'] = resultstr.strip()

            except IndexError:
                data['title'] = Match.replace_specile_chars(self.dom.title)
            data['title'] = str(data['title']).strip()

            article_body = ""

            allcontent = self.dom.find_all('article', class_="article-content font-normal")[0]

            big_ads = self.dom.find_all('div', class_="big_ad")
            #广告
            for ad in big_ads:
                allcontent = str(allcontent).replace(str(ad), '')


            nocontent = self.dom.find_all('div', class_="article-header")[0]



            content = str(allcontent).replace(str(nocontent),'',1)



            article_body += str(content)


            data['content'] = str(article_body)



            time_tationl = self.dom.select('div.byline time')[0]
            aut_tationl = self.dom.select('div.byline address')[0]


            date_time = datetime.datetime.strptime(str(time_tationl.text), '%Y年%m月%d日')

            print date_time.strftime('%Y-%m-%d')

            data['updated_time'] = date_time.strftime('%Y-%m-%d')


            data['author_name'] = str(aut_tationl.text)
            # print data['updated_time']

            data['voteup_count'] =  ""
            data['comment_count'] = ""

            data['image_url'] = ''

            data['author_id'] = 'meng-qing-xue-81'



            data['author_headline'] = ''
            data['author_avatar_url'] = 'https://pic4.zhimg.com/v2-38a89e42b40baa7d26d99cab9a451623_xl.jpg'
            data['author_gender'] = '0'
        except Exception as e:
            print e.message
            return []

        return data