#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from ...parser_tools import ParserTools


class YiibaiArticle(ParserTools):
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
        # TODO
        return answer_info

    def parse_info(self):
        self.parse_author_id()          # 获得博文作者id
        # self.parse_author_name()        # 获得博文作者名称
        self.parse_article_id()         # 获得article_id
        self.parse_article_title()      # 文章title
        self.parse_answer_content()     # 获得博文的内容
        # self.parse_href()
        # self.parse_comment()          # TODO
        # self.parse_publish_date()
        return self.info

    def parse_author_id(self):
        author_id = self.dom.select("div.list-group a.list-group-item ")[1]
        author_id = self.get_attr(author_id, 'href').split('/')[1]
        author_id = 'http://www.yiibai.com/' + author_id + '/'
        self.info['author_id'] = author_id

    def parse_article_id(self):
        article_id = self.dom.select("div.single-post-title h1")[0].get_text()
        self.info['article_id'] = str(article_id).replace('/', 'and')   # TODO remove ugly code

    def parse_author_name(self):
        self.info['author_name'] = self.info['author_id']

    def parse_article_title(self):
        self.info['title'] = self.info['article_id']

    def parse_answer_content(self):
        content = self.dom.select("div.content-body")[0]
        self.info['content'] = str(content)

    def parse_publish_date(self):
        # self.info['publish_date'] = u'TODO'
        pass