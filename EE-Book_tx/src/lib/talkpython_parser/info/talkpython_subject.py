#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from ...parser_tools import ParserTools
from ....tools.debug import Debug


class TalkPythonInfo(ParserTools):
    u"""
    parse page like this https://talkpython.fm/episodes/all, get base info
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
        # Debug.logger.debug(u"Getting talkpython info...")
        self.parse_base_info()         # basic user info: id, name, logo, description, article_num
        # self.parse_detail_info()     # detail_info, 博客等级, 积分, 访问, 关注人气
        return self.info

    def parse_base_info(self):
        self.parse_creator_id()
        self.parse_creator_name()
        # self.parse_description()
        # self.parse_article_count()
        self.parse_title()

    def parse_creator_id(self):
        u"""

        :return:
        """
        self.info['creator_id'] = 'https://talkpython.fm/episodes/all/'

    def parse_article_count(self):
        # # *TODO*
        u"""

        :return:
        """
        article_num = -1
        self.info['article_num'] = int(article_num)

    def parse_creator_name(self):
        self.info['creator_name'] = self.info['creator_id']

    def parse_description(self):
        # # *TODO*
        self.info['description'] = 'description'

    def parse_title(self):
        self.info['title'] = 'Talk Python To Me'
