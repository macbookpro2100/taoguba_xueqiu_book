# -*- coding: utf-8 -*-
from ...parser_tools import ParserTools
from ....tools.debug import Debug
from ....tools.match import Match


class SinaBlogAuthorInfo(ParserTools):
    u"""
    在用户档案页面进行解析, 获得博主基本信息
    """

    def __init__(self, dom=None):
        self.set_dom(dom)
        self.info = {}
        return

    def set_dom(self, dom):
        if dom:
            self.dom = dom
            # self.side_dom = dom.find('div', class_='SG_connBody')     # 首页的侧边栏, 有博客的基本信息
        return

    def get_info(self):
        self.parse_info()
        return self.info

    def parse_info(self):
        self.parse_base_info()        # 基本信息: 用户id, name, logo, description, article_num
        # self.parse_detail_info()      # 详细信息, 博客等级, 积分, 访问, 关注人气
        return self.info

    def parse_base_info(self):
        self.parse_creator_id()
        self.parse_creator_name()
        # self.parse_sign()
        self.parse_description()
        self.parse_logo()
        # self.parse_gender()
        # self.parse_article_count()
        return

    def parse_logo(self):
        u"""
        TODO: 速度有点慢, 暂时先这样写
        :return:
        """
        info_img = self.dom.select('div.info_img img')      # 获得头像地址 creator_logo
        if not info_img:
            return
        info_img_href = ParserTools.get_attr(info_img[0], 'real_src')
        if not info_img_href:
            Debug.logger.debug(u"用户头像没有找到")
            # TODO: 加一个默认的头像
            return
        self.info['creator_logo'] = info_img_href

    def parse_description(self):
        u"""
        个人简介的内容
        :return:
        """
        description = self.dom.select('table.personTable tbody tr td p')
        if not description:
            Debug.logger.debug(u"没有找到个人简介")
            # #dev log# bug report: https://github.com/knarfeh/SinaBlog2e-book/issues/1
            # 暂时的解决方式: 目前电子书内没有用到博主个人描述这一信息,这个问题的优先级不高,暂时不添加这一信息
            # 新浪博客的页面结构确实够混乱的,如果页面规律清晰可见当然花一点时间解决就可以了.不管怎么样,先放一放
            return
        description = u"EE-Book: 暂未添加"
        self.info['description'] = description

    def parse_creator_name(self):
        u"""
        "关于我"页面上, ownernick的内容
        :return:
        """
        creator_name = self.dom.select('div.info_nm span strong')       # 获得creator_name
        if not creator_name:
            Debug.logger.debug(u"没有找到博主姓名")
            return
        creator_name = creator_name[0].get_text().replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')
        self.info['creator_name'] = creator_name

    def parse_creator_id(self):
        u"""

        :return:
        """
        creator_id = self.dom.select('div.blognavInfo span a')
        if not creator_id:
            Debug.logger.debug(u"没有找到creator_id")
            return
        creator_id_href = ParserTools.get_attr(creator_id[1], 'href')    # 因为creator_id[0]是首页的链接

        if not creator_id_href:
            Debug.logger.debug(u"没有找到creator_id")
            # TODO
            return
        result = Match.sinablog_profile(creator_id_href)
        sinablog_id = result.group('sinablog_people_id')
        self.info['creator_id'] = sinablog_id