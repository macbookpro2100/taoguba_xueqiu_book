#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from ...parser_tools import ParserTools
from ....tools.debug import Debug


class JianshuCollectionInfo(ParserTools):
    u"""
    对 http://www.jianshu.com/collection/e83275c61b78 这样的页面进行解析, 得到简书某专题的基本信息
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
        Debug.logger.debug(u"Getting jianshu collection info...")
        self.parse_base_info()         # collection title, fake_id, real_id, description, follower
        # self.parse_detail_info()     # TODO ?
        return self.info

    def parse_base_info(self):
        self.parse_collection_real_id()
        self.parse_title()
        self.parse_collection_fake_id()
        self.parse_description()
        # self.parse_follower()         # WTF? not working?
        return

    def parse_title(self):
        title = str(self.dom.find("div", class_="header").h3.a.get_text())
        if not title:
            Debug.logger.debug(u'专题标题未找到')
        self.info['title'] = title
        return

    def parse_collection_fake_id(self):
        href = str(self.get_attr(self.dom.find("div", class_="header").h3.a, 'href'))
        collection_fake_id = str((href.split('/')[2])).strip()
        self.info['collection_fake_id'] = collection_fake_id
        return

    def parse_collection_real_id(self):
        u"""
        Need test
        :return:
        """
        real_id = self.get_attr(self.dom.select("div.header img.avatar")[0], "src").split("/")[5]
        self.info['collection_real_id'] = real_id
        return

    def parse_description(self):
        href = self.dom.find("div", class_="description").p.get_text().strip()
        self.info['description'] = unicode(href)
        return

    def parse_follower(self):
        following = self.dom.find("div", class_="following")
        span = following.select('span')[1]
        fo_num = span.get_text()
        self.info['follower'] = fo_num
        return
