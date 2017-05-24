#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from ...parser_tools import ParserTools


class TalkPythonArticle(ParserTools):
    def __init__(self, dom=None):
        self.set_dom(dom)
        self.info = {}
        return

    def set_dom(self, dom):
        if dom:
            self.dom = dom
        return

    def get_info(self):
        answer_info = self.parse_info()
        return answer_info

    def parse_info(self):
        self.parse_author_id()          # 获得博文作者id
        # self.parse_author_name()        # 获得博文作者名称
        self.parse_article_title()      # 文章title
        self.parse_article_id()         # 获得article_id
        self.parse_answer_content()     # 获得博文的内容
        # self.parse_href()
        # self.parse_comment()          # TODO
        # self.parse_publish_date()
        return self.info

    def parse_author_id(self):
        self.info['author_id'] = 'https://talkpython.fm/episodes/all/'

    def parse_article_id(self):
        from ....tools.extra_tools import ExtraTools
        article_id = ExtraTools.md5(self.info['title'])
        self.info['article_id'] = article_id

    def parse_author_name(self):
        self.info['author_name'] = self.info['author_id']

    def parse_article_title(self):
        try:
            title = self.dom.select('div.col-md-12 div h1')[0].get_text().replace('  ', '').replace('\n', '').split('#')

            title = title[1]
            title = title.replace(' ', '_').replace(':', '')
            self.info['title'] = title
        except IndexError:
            self.info['title'] = u"NO TITLE!!!!!!!!!"

    def parse_answer_content(self):
        try:
            content = self.dom.select('div.transcript-main div.large-content-text')[0]
            self.info['content'] = str(content)
        except IndexError:
            self.info['content'] = u"NO CONTENT!!!!"

    def parse_publish_date(self):
        # self.info['publish_date'] = u'TODO'
        pass

