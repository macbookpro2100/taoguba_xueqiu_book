#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from ...parser_tools import ParserTools


class CnblogArticle(ParserTools):
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
        author_id = self.get_attr(self.dom.select('h1.postTitle a')[0], 'href').split('/')[3]
        self.info['author_id'] = str(author_id)

    def parse_article_id(self):
        article_id = self.get_attr(self.dom.select('h1.postTitle a')[0], 'href').split('/')[-1].split('.')[0]
        self.info['article_id'] = str(article_id)

    def parse_author_name(self):
        pass

    def parse_article_title(self):
        title = self.dom.select('h1.postTitle a')[0].get_text()
        self.info['title'] = str(title)

    def parse_answer_content(self):
        content = self.dom.select('div#cnblogs_post_body')[0]
        self.info['content'] = str(content)

    def parse_publish_date(self):
        # self.info['publish_date'] = u'TODO'
        pass