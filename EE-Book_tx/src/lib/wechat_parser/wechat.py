# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from src.lib.wechat_parser.tools.parser_tools import ParserTools


class WechatColumnParser(ParserTools):
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


class WechatArticleParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'html.parser')

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
            time_dom = self.dom.find_all(id='publish_time', class_='rich_media_meta rich_media_meta_text')[0]

            print time_dom.text

            try:

                sf = self.dom.find_all('div', class_='StatsRow')[0]
                sf2 = self.dom.find_all('div', class_='StatsRow')[1]
                data['voteup_count'] = u"赞:{}".format(filter(str.isdigit, str(sf2.text)))
                data['comment_count'] = u"评论:{}".format(filter(str.isdigit, str(sf.text)))

            except IndexError as ie:
                data['voteup_count'] = ""
                data['comment_count'] = ""

            try:
                name_dom = self.dom.find_all(id='profileBt', class_='rich_media_meta rich_media_meta_nickname')[0]
                data['author_name'] = str(name_dom.text).strip()
            except IndexError as ie:
                data['author_name'] = '学习小组'

            data['updated_time'] = time_dom.text
            data['image_url'] = ''
            data['author_id'] = '525600'

            data['author_headline'] = ''
            data['author_avatar_url'] = ''
            data['author_gender'] = '0'
        except Exception as e:
            print e.message
            return []

        return data
