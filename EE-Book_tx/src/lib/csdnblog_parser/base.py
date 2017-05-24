#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from ..parser_tools import ParserTools
from content.csdnblog_article import CsdnBlogArticle


class BaseParser(ParserTools):
    u"""
    TODO: refactoring
    """
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'lxml')
        self.article_parser = CsdnBlogArticle()

    def get_answer_list(self):
        answer_list = []
        self.article_parser.set_dom(self.dom)
        answer_list.append(self.article_parser.get_info())
        return answer_list

    def get_extra_info(self):
        u"""

        :return:
        """