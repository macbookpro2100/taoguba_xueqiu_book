#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from ..tools.http import Http
from ..tools.match import Match

from page_worker import PageWorker
from ..lib.jianshu_parser.author import JianshuAuthorParser
from ..lib.jianshu_parser.collection import JianshuCollectionParser
from ..lib.jianshu_parser.notebooks import JianshuNotebooksParser

from ..lib.parser_tools import ParserTools

__all__ = [
    "JianshuAuthorWorker",
    "JianshuCollectionWorker",
    "JianshuNotebooksWorker",
]


class JianshuAuthorWorker(PageWorker):
    u"""
    for jianshu author
    """
    def create_save_config(self):
        config = {
            'jianshu_article': self.answer_list,
            'jianshu_info': self.question_list
        }
        return config

    def parse_content(self, content):
        parser = JianshuAuthorParser(content)
        self.answer_list += parser.get_answer_list()

    @staticmethod
    def parse_get_article_list(article_list_content):
        u"""
        获得每一篇博客的链接组成的列表
        :param article_list_content: 有博文目录的href的页面
        :return:
        """
        soup = BeautifulSoup(article_list_content, "lxml")
        article_list = soup.select('h4.title a')
        article_href_list = map(lambda x: 'http://www.jianshu.com'+ParserTools.get_attr(x, 'href'), article_list)
        return article_href_list

    def get_jianshu_question_list(self, target_url):
        u"""
        get jianshu_info, article_num, article_list
        :param target_url:
        :return:
        """
        index_content = Http.get_content(target_url)
        parser = JianshuAuthorParser(index_content)
        self.question_list += parser.get_extra_info()
        article_num = self.question_list[0]['article_num']      # not collection, only one author
        article_list = self.parse_get_article_list(index_content)
        return article_num, article_list

    def create_work_set(self, target_url):
        u"""
        根据target_url(例:http://www.jianshu.com/users/b1dd2b2c87a8/latest_articles)的内容,
        先获得creator_id, 再根据文章的数目, 获得页面数, 依次打开每个页面, 将文章的地址放入work_set中
        :param target_url:
        :return:
        """
        if target_url in self.task_complete_set:
            return
        id_result = Match.jianshu_author(target_url)
        jianshu_id = id_result.group('jianshu_id')
        article_num, article_list = self.get_jianshu_question_list(target_url)
        self.task_complete_set.add(target_url)
        if article_num % 9 != 0:
            page_num = article_num/9 + 1      # 9 href on one page
        else:
            page_num = article_num / 9

        for item in article_list:
            self.work_set.add(item)
        for page in range(page_num-1):          # page+2, don't need to get the first page
            url = 'http://www.jianshu.com/users/{}/latest_articles?page={}'.format(jianshu_id, page+2)
            content_article_list = Http.get_content(url)
            article_list = self.parse_get_article_list(content_article_list)
            for item in article_list:
                self.work_set.add(item)
        return


class JianshuCollectionWorker(PageWorker):
    u"""
    for jianshu collection
    """
    def add_property(self):
        self.collection_index_list = []

    @staticmethod
    def parse_max_page(content):
        soup = BeautifulSoup(content, 'lxml')
        div_info = soup.find_all('div',class_="info")[0]

        article_num = filter(str.isdigit,str(div_info.get_text().split(u'·')[0]))
        print article_num
        if article_num % 9 != 0:
            page_num = article_num/9 + 1      # 9 href on one page
        else:
            page_num = article_num / 9
        return page_num

    def create_work_set(self, target_url):
        if target_url in self.task_complete_set:
            return
        content = Http.get_content(target_url)
        if not content:
            return
        self.task_complete_set.add(target_url)
        real_id = self.info_list[0]['collection_real_id']
        fake_id = self.info_list[0]['collection_fake_id']
        page_num = self.parse_max_page(content)

        for page in range(page_num):
            url = 'http://www.jianshu.com/c/' + str(real_id) + '/notes?order_by=added_at&page={}'.format(page+1)
            content = Http.get_content(url)
            article_list = JianshuCollectionParser(content).get_article_list()
            self.add_collection_index(fake_id, article_list)
            for item in article_list:
                self.work_set.add(item)
        return

    def catch_info(self, target_url):
        if target_url in self.info_url_complete_set:
            return
        content = Http.get_content(target_url)
        if not content:
            return
        self.info_url_complete_set.add(target_url)
        parser = JianshuCollectionParser(content)
        self.info_list.append(parser.get_extra_info())
        return

    def parse_content(self, content):
        parser = JianshuAuthorParser(content)
        self.answer_list += parser.get_answer_list()

    def add_collection_index(self, collection_id, article_list):
        for item in article_list:
            data = {
                'href': item,
                'collection_fake_id': collection_id,
            }
            self.collection_index_list.append(data)
        return

    def create_save_config(self):
        config = {
            'jianshu_article': self.answer_list,
            'jianshu_collection_info': self.info_list,
            'jianshu_collection_index': self.collection_index_list,
        }
        return config


class JianshuNotebooksWorker(PageWorker):
    u"""
    for jianshu notebook
    """
    def add_property(self):
        self.notebooks_index_list = []

    @staticmethod
    def parse_max_page(content):
        soup = BeautifulSoup(content, 'lxml')
        article_num = int((soup.select("div.aside ul.meta a")[0].get_text().split(u"篇文章")[0].strip()))
        print u"article_num:" + str(article_num)
        if article_num % 9 != 0:
            page_num = article_num/9 + 1      # 9 href on one page
        else:
            page_num = article_num / 9
        return page_num

    def create_work_set(self, target_url):
        if target_url in self.task_complete_set:
            return
        content = Http.get_content(target_url)
        if not content:
            return
        self.task_complete_set.add(target_url)
        notebooks_id = self.info_list[0]['notebooks_id']
        page_num = self.parse_max_page(content)
        for page in range(page_num):
            url = 'http://www.jianshu.com/notebooks/627726/latest?page={}'.format(page+1)
            content = Http.get_content(url)
            article_list = JianshuNotebooksParser(content).get_article_list()
            self.add_notebooks_index(notebooks_id, article_list)
            for item in article_list:
                self.work_set.add(item)
        return

    def catch_info(self, target_url):
        if target_url in self.info_url_complete_set:
            return
        content = Http.get_content(target_url)
        if not content:
            return
        self.info_url_complete_set.add(target_url)
        parser = JianshuNotebooksParser(content)
        self.info_list.append(parser.get_extra_info())
        return

    def parse_content(self, content):
        parser = JianshuAuthorParser(content)
        self.answer_list += parser.get_answer_list()

    def add_notebooks_index(self, notebooks_id, article_list):
        for item in article_list:
            data = {
                'href': item,
                'notebooks_id': notebooks_id,
            }
            self.notebooks_index_list.append(data)
        return

    def create_save_config(self):
        config = {
            'jianshu_article': self.answer_list,
            'jianshu_notebooks_info': self.info_list,
            'jianshu_notebooks_index': self.notebooks_index_list,
        }
        return config


