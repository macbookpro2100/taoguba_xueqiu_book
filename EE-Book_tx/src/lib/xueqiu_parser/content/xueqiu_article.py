# -*- coding: utf-8 -*-
from ...parser_tools import ParserTools
from ....tools.match import Match
from ....tools.debug import Debug
import json
import time


class XueQiuArticle(ParserTools):
    def __init__(self, dom=None):
        self.set_dom(dom)
        self.info = {}
        return

    def set_dom(self, dom):
        if dom:
            self.dom = dom
        return

    def get_info(self):
        answer_info = self.parse_info()
        return answer_info

    def parse_info(self):
        self.parse_author_id()
        self.parse_author_name()
        self.parse_article_id()
        self.parse_article_title()
        self.parse_answer_content()  # 获得博文的内容
        # self.parse_href()
        self.parse_comment()  # TODO
        self.parse_publish_data()
        return self.info

    def parse_answer_content(self):
        u"""
        获得博文的内容
        :return:
        """
        article = json.loads(self.dom)
        article_body = article['text']

        if not article_body:
            Debug.logger.debug(u"博文内容没有找到")
            return

        article_body_with_time = str(article_body)

        creattime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(article['created_at'] / 1000)))
        lastedit = creattime if article['edited_at'] == None else time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
            float(article['edited_at'] / 1000)))

        self.info['content'] = article_body_with_time

    def parse_author_id(self):
        u"""
        获得author_id
        :return:
        """

        article = json.loads(self.dom)
        author_id = article['user_id']

        self.info['author_id'] = author_id

    def parse_author_name(self):
        u"""
        获得author的姓名
        :return:
        """
        article = json.loads(self.dom)
        author_name = article['user']['screen_name']  # 获得creator_name
        if not author_name:
            Debug.logger.debug(u"没有找到博主姓名")
            return
        self.info['author_name'] = author_name

    def parse_article_id(self):
        u"""
        获得博文的id
        :return:
        """
        article = json.loads(self.dom)
        id = article['id']
        self.info['article_id'] = id

    def parse_article_title(self):
        u"""
        获得博文的标题
        :return:
        """
        title_ = '回复'
        article = json.loads(self.dom)
        title_ = article['title']
        if title_.strip() == '':
            title_ = Match.stripTags(article['description'])[0:16]
        if title_.__len__() == 1:
            title_ = '|……'
        self.info['title'] = title_

    def parse_publish_data(self):
        u"""

        :return:
        """
        article = json.loads(self.dom)

        creattime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(article['created_at'] / 1000)))
        lastedit = creattime if article['edited_at'] == None else time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
            float(article['edited_at'] / 1000)))
        self.info['publish_date'] = str(lastedit)[:-3]

    def parse_comment(self):
        u"""
        :return:
        """
        article = json.loads(self.dom)

        self.info['comment'] = u"评论:{}".format(article['reply_count'])
        self.info['agree'] = u" 收藏:{}".format(article['fav_count'])
