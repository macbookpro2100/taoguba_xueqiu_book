# -*- coding: utf-8 -*-

from ..tools.type import Type
from initialbook import InitialBook


class Spider(object):
    def __init__(self):
        self.href = ''
        return


class SingleTask(object):
    u"""
    任务信息以对象属性方式进行存储
    """

    def __init__(self):
        self.kind = ''
        self.spider = Spider()
        self.book = InitialBook()
        return


class TaskPackage(object):
    u"""
    work_list: kind->single_task.href_index
    book_list: kind->single_task.book
    """
    def __init__(self):
        self.work_list = {}
        self.book_list = {}
        return

    def add_task(self, single_task=SingleTask()):
        if single_task.kind not in self.work_list:
            self.work_list[single_task.kind] = []
        self.work_list[single_task.kind].append(single_task.spider.href)

        if single_task.kind not in self.book_list:
            self.book_list[single_task.kind] = []
        self.book_list[single_task.kind].append(single_task.book)
        return

    def get_task(self):
        u"""
        jianshu_collection could not be merge, TODO: remove jianshu
        :return:
        """
        if Type.csdnblog_author in self.book_list:
            self.merge_csdnblog_article_book_list(book_type=Type.csdnblog_author)
        if Type.jianshu_author in self.book_list:
            self.merge_jianshu_article_book_list(book_type=Type.jianshu_author)
        if Type.sinablog_author in self.book_list:
            self.merge_sinablog_article_book_list(book_type=Type.sinablog_author)
        if Type.taoguba_author in self.book_list:
            self.merge_taoguba_article_book_list(book_type=Type.taoguba_author)
        if Type.xueqiu_author in self.book_list:
            self.merge_xueqiu_article_book_list(book_type=Type.xueqiu_author)
        if Type.answer in self.book_list:
            self.merge_question_book_list(book_type=Type.answer)
        if Type.question in self.book_list:
            self.merge_question_book_list(book_type=Type.question)
        if Type.article in self.book_list:
            self.merge_article_book_list()
        return self

    def merge_jianshu_article_book_list(self, book_type):
        book_list = self.book_list[book_type]
        book = InitialBook()
        info_extra = [item.sql.info_extra for item in book_list]
        article_extra = [item.sql.article_extra for item in book_list]
        book.kind = book_type
        print str([item.author_id for item in book_list])
        # book.author_id = '_'.join([item.author_id for item in book_list])
        book.sql.info = 'select * from jianshu_info where ({})'.format(' or '.join(info_extra))
        book.sql.article = 'select * from jianshu_article where ({})'.format(' or '.join(article_extra))
        book.sql.answer = 'select * from jianshu_article where ({})'.format(' or '.join(article_extra))
        self.book_list[book_type] = [book]
        return

    def merge_sinablog_article_book_list(self, book_type):
        book_list = self.book_list[Type.sinablog_author]
        book = InitialBook()
        info_extra = [item.sql.info_extra for item in book_list]
        article_extra = [item.sql.article_extra for item in book_list]
        book.kind = book_type
        book.author_id = '_'.join([item.author_id for item in book_list])
        book.sql.info = 'select * from sinablog_info where ({})'.format(' or '.join(info_extra))
        book.sql.article = 'select * from sinablog_article where ({})'.format(' or '.join(article_extra))
        book.sql.answer = 'select * from sinablog_article where ({})'.format(' or '.join(article_extra))
        self.book_list[book_type] = [book]
        return

    def merge_taoguba_article_book_list(self, book_type):
        book_list = self.book_list[Type.taoguba_author]
        book = InitialBook()
        info_extra = [item.sql.info_extra for item in book_list]
        article_extra = [item.sql.article_extra for item in book_list]
        book.kind = book_type
        book.author_id = '_'.join([item.author_id for item in book_list])
        book.sql.info = 'select * from taoguba_info where ({})'.format(' or '.join(info_extra))
        book.sql.article = 'select * from taoguba_article where ({})'.format(' or '.join(article_extra))
        book.sql.answer = 'select * from taoguba_article where ({})'.format(' or '.join(article_extra))
        self.book_list[book_type] = [book]
        return

    def merge_xueqiu_article_book_list(self, book_type):
        book_list = self.book_list[Type.xueqiu_author]
        book = InitialBook()
        info_extra = [item.sql.info_extra for item in book_list]
        article_extra = [item.sql.article_extra for item in book_list]
        book.kind = book_type
        book.author_id = '_'.join([item.author_id for item in book_list])
        book.sql.info = 'select * from xueqiu_info where ({})'.format(' or '.join(info_extra))
        book.sql.article = 'select * from xueqiu_article where ({})'.format(' or '.join(article_extra))
        book.sql.answer = 'select * from xueqiu_article where ({})'.format(' or '.join(article_extra))
        self.book_list[book_type] = [book]
        return

    def merge_csdnblog_article_book_list(self, book_type):
        book_list = self.book_list[Type.csdnblog_author]
        book = InitialBook()
        info_extra = [item.sql.info_extra for item in book_list]
        article_extra = [item.sql.article_extra for item in book_list]
        book.kind = book_type
        book.author_id = '_'.join([item.author_id for item in book_list])
        book.sql.info = 'select * from csdnblog_info where ({})'.format(' or '.join(info_extra))
        book.sql.article = 'select * from csdnblog_article where ({})'.format(' or '.join(article_extra))
        book.sql.answer = 'select * from csdnblog_article where ({})'.format(' or '.join(article_extra))
        self.book_list[book_type] = [book]
        return

    def merge_article_book_list(self):
        book_list = self.book_list[Type.article]
        book = InitialBook()
        answer = [item.sql.answer for item in book_list]
        info = [item.sql.info for item in book_list]
        book.kind = Type.article
        book.sql.info = 'select * from Article where ({})'.format(' or '.join(info))
        book.sql.answer = 'select * from Article where ({})'.format(' or '.join(answer))
        self.book_list[Type.article] = [book]
        return

    def merge_question_book_list(self, book_type):
        book_list = self.book_list[book_type]
        book = InitialBook()
        question = [item.sql.question for item in book_list]
        answer = [item.sql.answer for item in book_list]
        info = [item.sql.info for item in book_list]
        book.kind = book_type
        book.sql.info = 'select * from Question where ({})'.format(' or '.join(info))
        book.sql.question = 'select * from Question where ({})'.format(' or '.join(question))
        book.sql.answer = 'select * from Answer where ({})'.format(' or '.join(answer))
        self.book_list[book_type] = [book]
        return

    def is_work_list_empty(self):
        for kind in Type.type_list:
            if self.work_list.get(kind):
                return False
        return True

    def is_book_list_empty(self):
        for kind in Type.type_list:
            if self.book_list.get(kind):
                return False
        return True
