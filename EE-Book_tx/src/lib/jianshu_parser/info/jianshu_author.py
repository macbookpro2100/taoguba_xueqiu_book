#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from ...parser_tools import ParserTools
from ....tools.debug import Debug


class JianshuAuthorInfo(ParserTools):
    u"""
    对 http://www.jianshu.com/users/b1dd2b2c87a8/latest_articles 这样的页面进行解析, 获得作者基本信息
    """

    def __init__(self, dom=None):
        self.set_dom(dom)
        self.info = {}
        self.dom = None
        return

    def set_dom(self, dom):
        if dom:
            self.dom = dom
        return

    def get_info(self):
        self.parse_info()
        return self.info

    def parse_info(self):
        Debug.logger.debug(u"getting jianshu author info...")
        self.parse_base_info()         # basic user info: id, name, logo, description, article_num
        # self.parse_detail_info()     # detail_info, 博客等级, 积分, 访问, 关注人气
        return self.info

    def parse_base_info(self):
        self.parse_creator_id()
        self.parse_creator_name()
        # self.parse_sign()
        self.parse_description()
        # self.parse_logo()
        # self.parse_gender()
        self.parse_article_count()

        return

    def parse_creator_id(self):
        u"""

        :return:
        """
        creator_id = str(self.dom.find("div", class_="basic-info").h3.a['href'][7:])
        if not creator_id:
            Debug.logger.info(u"没有找到creator_id")
        Debug.logger.debug(u"parse_creator_id中, creator_id为:" + str(creator_id))
        self.info['creator_id'] = creator_id

    def parse_article_count(self):
        u"""

        :return:
        """
        article_num = self.dom.select('ul.clearfix li b')
        if not article_num:
            Debug.logger.info(u"没有找到文章的数量")
        article_num = article_num[2].get_text()      # 第3个是文章数量
        Debug.logger.debug(u"文章数量为:" + str(article_num))
        self.info['article_num'] = int(article_num)

    def parse_logo(self):
        u"""

        :return:
        """
        pass

    def parse_description(self):
        u"""

        :return:
        """
        descirption = self.dom.select('p.intro')
        if not descirption:
            Debug.logger.info(u"没有找到博主的描述")
        descirption = descirption[0].get_text().replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')
        Debug.logger.debug(u"description为:" + str(descirption))
        self.info['description'] = descirption

    def parse_creator_name(self):
        u"""

        :return:
        """
        creator_name = self.dom.select('div.basic-info h3 a')
        if not creator_name:
            Debug.logger.info(u"没有找到博主姓名")
        creator_name = creator_name[0].get_text().replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')
        Debug.logger.debug(u"creator_name为:" + str(creator_name))
        self.info['creator_name'] = creator_name



