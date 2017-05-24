#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from base import BaseParser
from info.talkpython_subject import TalkPythonInfo


class TalkPythonParser(BaseParser):
    def get_article_list(self):
        content = self.dom.select("tbody tr td a")
        article_list = map(lambda x: 'https://talkpython.fm'+self.get_attr(x, 'href').replace('show', 'transcript'),
                           content)
        return article_list

    def get_extra_info(self):
        author_parser = TalkPythonInfo()     # generic_info 表中的信息
        author_parser.set_dom(self.dom)
        return author_parser.get_info()
