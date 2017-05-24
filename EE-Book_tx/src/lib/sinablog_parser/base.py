# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from ..parser_tools import ParserTools
from content.sinablog_article import SinaBlogArticle


class BaseParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'lxml')
        self.article_parser = SinaBlogArticle()

    def get_answer_list(self):
        answer_list = []
        self.article_parser.set_dom(self.dom)
        answer_list.append(self.article_parser.get_info())
        return answer_list

    def get_extra_info(self):
        u"""
        扩展功能: 获取扩展信息, 需要重载使用, 被author.py重载了
        :return:
        """