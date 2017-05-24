#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from ...parser_tools import ParserTools
from ....tools.debug import Debug


class CsdnBlogAuthorInfo(ParserTools):
    u"""

    """
    def __init__(self, dom=None):
        self.dom = None
        self.set_dom(dom)
        self.info = {}
        return

    def set_dom(self, dom):
        if dom:
            self.dom = dom
        return

    def get_info(self):
        self.parse_info()
        return self.info

    def parse_info(self):
        Debug.logger.debug(u"getting author info...")
        self.parse_base_info()
        return self.info

    def parse_base_info(self):
        self.parse_creator_id()
        self.parse_creator_name()
        # self.parse_sign()
        self.parse_description()
        # self.parse_logo()
        # self.parse_gender()
        self.parse_article_count()

    def parse_creator_id(self):
        creator_id = self.dom.find('a', class_='user_name')
        if not creator_id:
            Debug.logger.info(u"没有找到creator_id")
        self.info['creator_id'] = creator_id.get_text()

    def parse_creator_name(self):
        u"""
        blog title
        :return:
        """
        try:
            blog_title = self.dom.find('div', id='blog_title').h2.a.get_text()
        except:
            Debug.logger.debug(u"没有找到blog_title")    # TODO: far from awesome
            return
        self.info['creator_name'] = blog_title

    def parse_sign(self):
        pass

    def parse_description(self):
        blog_desc = self.dom.find('div', id='blog_title').h3.get_text()
        self.info['description'] = blog_desc

    def parse_logo(self):
        pass

    def parse_gender(self):
        pass

    def parse_article_count(self):
        article_num_li = self.dom.select('ul#blog_statistics li span')
        article_num = 0
        for i in range(len(article_num_li)-1):
            text = article_num_li[i].get_text()
            now_article_num = text[:text.rfind(u"篇")]
            article_num += int(now_article_num)
        self.info['article_num'] = int(article_num)
