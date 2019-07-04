# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from src.lib.wechat_parser.tools.parser_tools import ParserTools
from src.tools.config import Config
from src.tools.match import Match
import datetime

import time

class Todo3ColumnParser(ParserTools):
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


class Todo3ArticleParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'lxml')

    def get_article_info(self):
        data = {}
        try:

            try:
                title_tationl  = self.dom.select('h1.item-name')[0]
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

            allcontent = self.dom.find_all('article', id="articleId")[0]

            title_ads = self.dom.find_all('h1', class_="item-name")[0]
            ah_ads = self.dom.find_all('h2', class_="z-clearfix")[0]
            head_ads = self.dom.find_all('div', class_="recommend-tab z-clearfix item-preferential")[0]

            allcontent = str(allcontent).replace(str(title_ads), '')
            allcontent = str(allcontent).replace(str(head_ads), '')

            data['content'] = str(allcontent)





            timeH  = head_ads.find_all('span')[0]
            timeHs = timeH.find_all('span')


            time_tationl = (timeHs[0].text)[0:16]

            print time_tationl


            data['updated_time'] = time_tationl


            data['author_name'] = str(ah_ads.text)
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