# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from base import BaseParser
from content.xueqiu_article import XueQiuArticle
from info.xueqiu_author import XueQiuAuthorInfo


class XueQiuArticleParser(BaseParser):
    u"""
    获得sinablog_info表中所需的内容
    """
    def __init__(self, content):
        strarticle=  str(content).replace("\'", '"',1000)
        self.dom =  strarticle
        self.article_parser = XueQiuArticle(strarticle) #雪球
        return



