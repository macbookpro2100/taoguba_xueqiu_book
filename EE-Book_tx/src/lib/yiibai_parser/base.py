#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from ..parser_tools import ParserTools
from content.yiibai_article import YiibaiArticle


class BaseParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'lxml')
        self.article_parser = YiibaiArticle()

    def get_answer_list(self):
        answer_list = []
        self.article_parser.set_dom(self.dom)
        answer_list.append(self.article_parser.get_info())
        return answer_list

    def get_extra_info(self):
        u"""
        e.g. base info of Yiibai
        :return:
        """
        pass
