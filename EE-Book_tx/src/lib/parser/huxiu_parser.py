# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from src.lib.wechat_parser.tools.parser_tools import ParserTools

from src.tools.match import Match


class HuXiuColumnParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'html.parser')

    def get_column_info(self):
        data = {}



        data['article_count'] = 0
        data['follower_count'] = 0
        data['description'] = ''
        data['image_url'] = ''

        return data


class HuXiuArticleParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'lxml')

    def get_article_info(self):
        data = {}
        try:
            try:
                list_articl_title = self.dom.find_all('h1', class_="t-h1")[0]
                title = str(list_articl_title.text)
                if title.__contains__('/'):
                    title = Match.replace_specile_chars(title)
                data['title'] = title
            except IndexError:
                data['title'] = self.dom.title
            print data['title']
            data['title'] = str(data['title']).strip()

            article_body = ""

            list_article_content = self.dom.find_all('div', class_='article-content-wrap')
            for tgo in list_article_content:
                main_context = ''
                list_articl_img = self.dom.find_all('div', class_="article-img-box")[0]
                list_articl_info = self.dom.find_all('span', class_="article-time")[0]
                list_articl_author_name = self.dom.find_all('span', class_="author-name")[0]
                list_articl_share = self.dom.find_all('span', class_="article-share")[0]
                list_articl_pl = self.dom.find_all('span', class_="article-pl")[0]
                print list_articl_author_name.text

                data['author_name'] = list_articl_author_name.text

                data['voteup_count'] =  u"{}".format(list_articl_pl)
                data['comment_count'] = u"{}".format(list_articl_share)
                # 保留主内容
                list_content = tgo.find_all('div', class_="neirong-shouquan-public")
                for tgo_public in list_content:
                    tgo_public.clear()
                main_context = str(list_articl_img) + str(tgo)

                article_body += main_context

            data['content'] = str(article_body)


            data['updated_time'] = str((self.dom.find_all('span', class_="article-time")[0]).text)

            # print data['updated_time']

            data['image_url'] = ''

            data['author_id'] = 'meng-qing-xue-81'

            data['author_headline'] = ''
            data['author_avatar_url'] = 'https://pic4.zhimg.com/v2-38a89e42b40baa7d26d99cab9a451623_xl.jpg'
            data['author_gender'] = '0'
        except Exception as e:
            print e.message
            return []

        return data