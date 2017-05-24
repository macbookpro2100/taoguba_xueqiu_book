#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from ...parser_tools import ParserTools
from ....tools.debug import Debug


class CnblogsAuthorInfo(ParserTools):
    u"""
    parse page like this http://www.cnblogs.com/buptzym/, got base info of author
    """

    def __init__(self, dom=None):
        self.set_dom(dom)
        self.info = {}
        self.dom = None
        return

    def set_dom(self, dom):
        if dom:
            self.dom = dom
        return

    def get_info(self):
        self.parse_info()
        return self.info

    def parse_info(self):
        Debug.logger.debug(u"getting cnblogs author info...")
        self.parse_base_info()         # basic user info: id, name, logo, description, article_num
        # self.parse_detail_info()     # detail_info, 博客等级, 积分, 访问, 关注人气
        return self.info

    def parse_base_info(self):
        self.parse_creator_id()
        self.parse_creator_name()
        # self.parse_description()
        self.parse_article_count()
        self.parse_title()

    def parse_creator_id(self):
        u"""

        :return:
        """
        creator_id = self.get_attr(self.dom.find('a', class_='headermaintitle'), 'href').split('/')[3]
        self.info['creator_id'] = creator_id

    def parse_article_count(self):
        u"""

        :return:
        """
        article_num = self.dom.find('div', class_='blogStats').get_text().strip().replace(' ', '').split(u'随笔-')
        article_num = article_num[1].split(u'文章-')[0]
        self.info['article_num'] = int(article_num)

    def parse_creator_name(self):
        creator_name = self.dom.find('a', class_='headermaintitle').get_text()
        self.info['creator_name'] = str(creator_name)

    def parse_description(self):
        self.info['description'] = 'description'

    def parse_title(self):
        self.info['title'] = self.info['creator_name']
