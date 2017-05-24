#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from ...parser_tools import ParserTools
from ....tools.match import Match
from ....tools.debug import Debug


class JianshuArticle(ParserTools):
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
        self.parse_author_name()        # 获得博文作者名称
        self.parse_article_id()         # 获得article_id
        self.parse_article_title()      # 文章title
        self.parse_answer_content()     # 获得博文的内容
        self.parse_href()
        # self.parse_comment()          # TODO
        self.parse_publish_date()
        return self.info

    def parse_author_id(self):          # TODO delete?这个部分可以不重复的
        u"""
        获得author_id
        :return:
        """
        author_id = str(self.dom.find("div", class_="author-info").find("a", class_="avatar")['href'][7:])
        if not author_id:
            Debug.logger.info(u"没有找到文章作者id")
        self.info['author_id'] = author_id

    def parse_author_name(self):        # TODO: 这部分也没有必要
        author_name = str(self.dom.find("a", class_="author-name").span.get_text())
        if not author_name:
            Debug.logger.info(u"没有找到文章作者名称")
            return
        self.info['author_name'] = author_name

    def parse_article_id(self):
        article_id = str(self.dom.find("div", class_="share-group"))
        if not article_id:
            Debug.logger.info(u"没有找到文章id")
            return
        result = Match.jianshu_article_id(article_id)
        article_id = result.group('jianshu_article_id')
        self.info['article_id'] = article_id

    def parse_article_title(self):
        title = str(self.dom.find("title").get_text())
        if not title:
            Debug.logger.info(u"没有找到文章标题")
            return
        self.info['title'] = title

    def parse_answer_content(self):
        content = str(self.dom.find("div", class_="show-content"))
        if not content:
            Debug.logger.info(u"没有找到文章内容")
            return
        self.info['content'] = content

    def parse_href(self):
        content = str(self.dom.find("meta", property="twitter:url")['content'])
        # TODO: test the code
        if not content:
            Debug.logger.info(u"没有找到文章href")
            return
        self.info['href'] = content

    def parse_publish_date(self):
        content = str(self.dom.find("div", class_="author-info").findAll("span")[3].get_text())
        if not content:
            Debug.logger.info(u"没有找到文章更新时间")
        self.info['publish_date'] = self.parse_date(content[:10].replace('.', '-'))
