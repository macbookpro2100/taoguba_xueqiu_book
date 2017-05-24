# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from base import BaseParser
from content.xueqiu_article import XueQiuArticle
from info.xueqiu_author import XueQiuAuthorInfo


class XueQiuParser(BaseParser):
    u"""
    获得sinablog_info表中所需的内容
    """
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'lxml')
        self.article_parser = XueQiuArticle(str(content)) #雪球

        return

    def get_extra_info(self):
        author_parser = XueQiuAuthorInfo()     # xueqiu_info表中的信息
        author_parser.set_dom(self.dom)
        return [author_parser.get_info()]

