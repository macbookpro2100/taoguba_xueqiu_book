# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from base import BaseParser
from content.taoguba_article import TGBArticle
from info.taoguba_author import TGBAuthorInfo


class TGBParser(BaseParser):
    u"""
    获得sinablog_info表中所需的内容
    """
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'lxml')
        self.article_parser = TGBArticle(self.dom)

        return

    def get_extra_info(self):
        author_parser = TGBAuthorInfo()     # TGB_info表中的信息
        author_parser.set_dom(self.dom)
        return [author_parser.get_info()]

