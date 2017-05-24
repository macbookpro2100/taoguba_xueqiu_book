#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from base import BaseParser
from info.jianshu_notebooks import JianshuNotebooksInfo


class JianshuNotebooksParser(BaseParser):

    def get_article_list(self):
        article_list = self.dom.select("div h4.title a")
        article_href_list = map(lambda x: 'http://www.jianshu.com'+self.get_attr(x, 'href'), article_list)
        return article_href_list

    def get_extra_info(self):
        parser = JianshuNotebooksInfo()
        parser.set_dom(self.dom)
        return parser.get_info()
