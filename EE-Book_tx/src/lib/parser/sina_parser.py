# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from src.lib.wechat_parser.tools.parser_tools import ParserTools
from src.tools.debug import Debug


class SinaColumnParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'lxml')

    def get_column_info(self):
        data = {}
        u"""
        "关于我"页面上, ownernick的内容
        :return:
        """
        creator_name = self.dom.select('div.info_nm span strong')  # 获得creator_name
        if not creator_name:
            Debug.logger.debug(u"没有找到博主姓名")
            return
        creator_name = creator_name[0].get_text().replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')

        data['title'] = creator_name

        data['article_count'] = 0
        data['follower_count'] = 0
        data['description'] = ''
        data['image_url'] = ''

        return data


class SinaArticleParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'lxml')

    def get_article_info(self):
        data = {}
        try:
            u"""
            获得博文的标题
            :return:
            """
            article_title = False
            title = self.dom.select('div.articalTitle h2')
            if title:
                article_title = title[0].get_text()
            if not article_title:
                Debug.logger.debug(u"没有找到博文标题")
                return
            # 标题里如果出现&,<<这样的符号会出错

            data['title'] = str(article_title).replace('&', '&amp;').replace('<<', "《").replace('>>', "》")

            u"""
            获得博文的内容
            :return:
            """
            article_body = self.dom.find('div', class_='articalContent')
            # article_body = self.dom.find('div', class_='articalContent')
            # article_body = self.dom.find('div', id='sina_keyword_ad_area2')
            # article_body = self.dom.select('#sina_keyword_ad_area2')[0]
            # article_body = self.dom.select('div.articalContent')
            if not article_body:
                Debug.logger.debug(u"博文内容没有找到")
                return
            article_body = str(article_body)
            data['content'] = article_body


            time_tile = self.dom.find_all('span', class_="time SG_txtc")

            data['updated_time'] = time_tile[0].text
            data['voteup_count'] = u"{}".format('')
            data['image_url'] = ''
            data['comment_count'] = u"{}".format('')

            u"""
            获得博文的id
            :return:
            """
            article_id = False
            id = self.dom.select('div.artical h2')
            if id:
                article_id = ParserTools.get_attr(id[0], 'id')
            if not article_id:
                Debug.logger.debug(u"没有找到博文的id")
                return
            article_id = article_id[2:]
            data['author_id'] = article_id
            u"""
            获得author的姓名
            :return:
            """
            author_name = self.dom.select('div.info_nm span strong')  # 获得creator_name
            if not author_name:
                Debug.logger.debug(u"没有找到博主姓名")
                return
            author_name = author_name[0].get_text().replace(' ', '').replace('\n', '').replace('\t', '').replace('\r',
                                                                                                                 '')
            data['author_name'] = author_name
            data['author_headline'] = ''
            data['author_avatar_url'] = ''
            data['author_gender'] = '0'
        except Exception as e:
            print e.message
            return []

        return data
