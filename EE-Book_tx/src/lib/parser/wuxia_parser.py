# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from src.lib.wechat_parser.tools.parser_tools import ParserTools
from src.tools.config import Config
from src.tools.match import Match


class WuXiaColumnParser(ParserTools):
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


class WuXiaArticleParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'lxml')

    def get_article_info(self):
        data = {}
        try:

            try:
                title_tationl = self.dom.find_all('h1', class_="article-title")
                # print  u"标题 {}".format(span_dom.text.strip()),
                resultstr = title_tationl[0].text


                if resultstr.__contains__('/'):
                    resultstr = Match.replace_specile_chars(resultstr)
                data['title'] = resultstr

                data['title'] = resultstr.strip()

            except IndexError:
                data['title'] = Match.replace_specile_chars(self.dom.title)
            data['title'] = str(data['title']).strip()

            article_body = ""

            content = self.dom.find_all('article', class_="article-content")[0]

 

            article_body += str(content)


            strOfinfos=self.dom.find_all('p', style="text-align: center;")
            for x in strOfinfos:
                article_body = article_body.replace(str(x),'',1)

            data['content'] = str(article_body)

            time_tationl = self.dom.find_all('div', class_="article-meta")[0]

            data['updated_time'] = time_tationl.find_all('span', class_="item")[0].text

            # print data['updated_time']

            data['voteup_count'] =  ""
            data['comment_count'] = ""

            data['image_url'] = ''

            data['author_id'] = 'meng-qing-xue-81'

            tempName = time_tationl.find_all('span', class_="item")[1].text

            data['author_name'] = (str(tempName).split('：'))[-1]
            data['author_headline'] = ''
            data['author_avatar_url'] = 'https://pic4.zhimg.com/v2-38a89e42b40baa7d26d99cab9a451623_xl.jpg'
            data['author_gender'] = '0'
        except Exception as e:
            print e.message
            return []

        return data