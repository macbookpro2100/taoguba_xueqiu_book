#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from bs4 import BeautifulSoup

from ..tools.http import Http
from ..tools.match import Match
from ..lib.parser_tools import ParserTools
from ..lib.csdnblog_parser.csdnblog_parser import CsdnBlogParser
from page_worker import PageWorker

__all__ = [
    "csdnAuthorWorker"
]


class csdnAuthorWorker(PageWorker):
    u"""
    csdn blog
    """
    @staticmethod
    def parse_max_page(content):
        u"""
        :param content: index page
        :return: max page
        """
        max_page = 1
        dom = BeautifulSoup(content,"lxml")
        indexNum = dom.find_all('div',class_="pagelist")[0]
        indurl = indexNum.findAll('a')[-1]
        max_page = int(str(indurl.get('href')).split('/')[-1])
        return max_page

    def create_save_config(self):
        config = {'csdnblog_article': self.answer_list, 'csdnblog_info': self.question_list}
        return config

    def parse_content(self, content):
        parser = CsdnBlogParser(content)
        self.answer_list += parser.get_answer_list()

    @staticmethod
    def parse_get_article_list(article_list_content):
        u"""
        get the list of blog href
        :param article_list_content
        :return: list page
        """
        soup = BeautifulSoup(article_list_content, 'lxml')
        article_href_list = []

        article_list = soup.select('span.link_title a')
        for item in range(len(article_list)):
            article_href = 'http://blog.csdn.net'+str(ParserTools.get_attr(article_list[item], 'href'))
            article_href_list.append(article_href)
        return article_href_list

    def get_csdnblog_question_list(self, index_content):
        u"""
        get csdnblog author info, get article_num, article_list
        :param index_content:
        :return:
        """
        parser = CsdnBlogParser(index_content)
        self.question_list += parser.get_extra_info()
        article_num = self.question_list[0]['article_num']
        article_list = self.parse_get_article_list(index_content)
        return article_num, article_list

    def create_work_set(self, target_url):
        u"""

        :param target_url: http://blog.csdn.net/dbzhang800
        :return:
        """
        if target_url in self.task_complete_set:
            return
        id_result = Match.csdnblog_author(target_url)
        csdn_author_id = id_result.group('csdnblog_author_id')
        index_content = Http.get_content(target_url)
        article_num, article_list = self.get_csdnblog_question_list(index_content)
        page_num = int(self.parse_max_page(index_content))
        self.task_complete_set.add(target_url)

        for item in article_list:
            self.work_set.add(item)
        for page in range(page_num-1):    # page+2, don't need to get the first page
            url = 'http://blog.csdn.net/{}/article/list/{}'.format(csdn_author_id, page+2)
            content = Http.get_content(url)
            _, article_list = self.get_csdnblog_question_list(content)
            for item in article_list:
                self.work_set.add(item)
        return



