# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from src.lib.wechat_parser.tools.parser_tools import ParserTools


class HuaWeiColumnParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'html.parser')

    def get_column_info(self):
        data = {}
        title_dom = self.dom.select('div.topic_name_editor h1.inline span')[0]
        data['title'] = title_dom.get_text()

        data['article_count'] = 0
        data['follower_count'] = 0
        data['description'] = ''
        data['image_url'] = ''

        return data


class HuaWeiArticleParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'lxml')

    def get_article_info(self):
        data = {}
        try:
            title = self.dom.select('div#page-content h2.rich_media_title')
            if len(title) == 0:
                return []
            if str(title[0].get_text()).__contains__('Are you a robot'):
                return []
            data['title'] = title[0].get_text()
            content_dom = self.dom.select('div#page-content div.rich_media_content')[0]
            data['content'] = self.get_tag_content(content_dom)
            time_dom = self.dom.find_all(id='post-date', class_='rich_media_meta rich_media_meta_text')[0]

            print time_dom.text


            sf = self.dom.find_all('div',class_='StatsRow')[0]
            sf2 = self.dom.find_all('div',class_='StatsRow')[1]

            data['updated_time'] = time_dom.text
            data['voteup_count'] = filter(str.isdigit, str(sf2.text))
            data['image_url'] = ''
            data['comment_count'] = filter(str.isdigit, str(sf.text))
            data['author_id'] = 'meng-qing-xue-81'
            data['author_name'] = '知乎助手'
            data['author_headline'] = '微信魔改版'
            data['author_avatar_url'] = 'https://pic4.zhimg.com/v2-38a89e42b40baa7d26d99cab9a451623_xl.jpg'
            data['author_gender'] = '0'
        except Exception as e:
            print e.message
            return []

        return data