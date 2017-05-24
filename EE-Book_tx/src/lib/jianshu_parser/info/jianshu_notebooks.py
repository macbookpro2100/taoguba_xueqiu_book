#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from ...parser_tools import ParserTools
from ....tools.debug import Debug


class JianshuNotebooksInfo(ParserTools):
    u"""
    对 http://www.jianshu.com/notebooks/627726/latest 这样的页面进行解析, 得到简书某文集的基本信息
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
        print u"nothing? ha?"
        return self.info

    def parse_info(self):
        Debug.logger.debug(u"Getting jianshu notebooks info...")
        self.parse_base_info()         # notebooks title, notebooks_id, author_name, description, follower
        # self.parse_detail_info()     # TODO ?
        return self.info

    def parse_base_info(self):
        self.parse_notebooks_id()
        self.parse_title()
        self.parse_author_name()
        # self.parse_description()
        self.parse_follower()         # WTF? not working?
        return

    def parse_title(self):
        title = self.dom.select("div.aside h3.title a")[0].get_text()
        self.info['title'] = title
        return

    def parse_notebooks_id(self):
        notebooks_id = self.get_attr(self.dom.select("div.aside h3.title a")[0], 'href').split('/')[2]
        self.info['notebooks_id'] = notebooks_id
        return

    def parse_author_name(self):
        author_name = self.dom.select('div.author a')[1].get_text()
        self.info['author_name'] = author_name
        return

    def parse_description(self):
        return

    def parse_follower(self):
        follower = self.dom.select("div.aside ul.meta a")[1].get_text().split(u"人关注")[0].strip()
        self.info['follower'] = int(follower)
        return
