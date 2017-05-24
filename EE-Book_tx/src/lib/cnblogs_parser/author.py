#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from base import BaseParser
from info.cnblogs_author import CnblogsAuthorInfo


class CnblogsAuthorParser(BaseParser):

    def get_article_list(self):
        article_list = self.dom.select('div.postTitle a.postTitle2')
        article_href_list = map(lambda x: self.get_attr(x, 'href'), article_list)
        return article_href_list

    def get_extra_info(self):
        author_parser = CnblogsAuthorInfo()     # jianshu_author表中的信息
        author_parser.set_dom(self.dom)
        return author_parser.get_info()
