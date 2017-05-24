#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from base import BaseParser
from info.yiibai_subject import YiibaiInfo


class YiibaiParser(BaseParser):

    def get_article_list(self):
        article_list = self.dom.select("div.list-group a.list-group-item")
        article_list = map(lambda x: 'http://www.yiibai.com'+self.get_attr(x, 'href'), article_list)
        article_list[0] = 'http://www.yiibai.com/'+article_list[1].split('/')[3]
        return article_list

    def get_extra_info(self):
        author_parser = YiibaiInfo()     # generic_info 表中的信息
        author_parser.set_dom(self.dom)
        return author_parser.get_info()
