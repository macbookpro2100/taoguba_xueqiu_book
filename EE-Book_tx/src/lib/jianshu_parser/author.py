#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from base import BaseParser
from info.jianshu_author import JianshuAuthorInfo


class JianshuAuthorParser(BaseParser):
    def get_extra_info(self):
        author_parser = JianshuAuthorInfo()     # jianshu_author表中的信息
        author_parser.set_dom(self.dom)
        return [author_parser.get_info()]