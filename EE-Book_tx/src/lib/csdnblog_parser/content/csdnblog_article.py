#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from ...parser_tools import ParserTools
from ....tools.debug import Debug


class CsdnBlogArticle(ParserTools):
    def __init__(self, dom):
        self.dom = None
        self.set_dom(dom)
        self.info = {}

    def set_dom(self, dom):
        if dom:
            self.dom = dom
        return

    def get_info(self):
        answer_info = self.parse_info()
        return answer_info

    def parse_info(self):
        self.parse_author_id()
        self.parse_author_name()
        self.parse_article_id()
        self.parse_article_title()
        self.parse_article_content()
        self.parse_publish_date()
        return self.info

    def parse_author_id(self):
        u"""

        :return:
        """
        author_id = self.dom.find('a', class_='user_name')
        if not author_id:
            Debug.logger.info(u"没有找到creator_id")
        self.info['author_id'] = author_id.get_text()

    def parse_author_name(self):
        u"""

        :return:
        """
        try:
            blog_title = self.dom.find('div', id='blog_title').h2.a.get_text()
        except:
            Debug.logger.debug(u"没有找到blog_title")    # TODO: far from awesome
            return
        self.info['author_name'] = blog_title

    def parse_article_id(self):
        u"""

        :return:
        """
        article_href_list = self.dom.select('span.link_title a')
        if not article_href_list:
            Debug.logger.debug(u"没有找到文章ID")
        article_href = ParserTools.get_attr(article_href_list[0], 'href')
        article_id = article_href.split('/')[-1]
        self.info['article_id'] = article_id

    def parse_article_title(self):
        u"""

        :return:
        """
        article_title_list = self.dom.select('span.link_title a')
        if not article_title_list:
            Debug.logger.debug(u"没有找到文章标题")
            return
        article_title = article_title_list[0].get_text().replace(' ', '').replace('\n', '').replace('\r', '')
        self.info['title'] = str(article_title)

    def parse_article_content(self):
        u"""

        :return:
        """
        article_content = self.dom.find('div', id='article_content')
        if not article_content:
            Debug.logger.debug(u"没有找到文章")
            return
        self.info['content'] = str(article_content)

    def parse_publish_date(self):
        u"""

        :return:
        """
        article_content = self.dom.find('span', class_='link_postdate').get_text()
        if not article_content:
            Debug.logger.debug(u"没有找到发布日期")
            return
        postdate = article_content[:10]

        read_content = self.dom.find('span', class_='link_view').get_text()

        comit_content = self.dom.find('span', class_='link_comments').get_text()

        self.info['comment'] = u"阅读:{}".format(filter(str.isdigit, str(read_content)))
        self.info['agree'] = u"{}".format(comit_content)
        self.info['publish_date'] = str(postdate)
