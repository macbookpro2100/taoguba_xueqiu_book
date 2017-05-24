#!/usr/bin/env python
# -*- coding: utf-8 -*-

from taoguba_image import ImageContainer
# from image  import ImageContainer
from ..tools.config import Config
from ..tools.db import DB
from ..tools.match import Match
from ..tools.type import Type


class InitialBook(object):
    class Sql(object):
        def __init__(self):
            self.question = ''
            self.answer = ''
            self.info = ''
            self.article = ''
            self.info_extra = ''
            self.article_extra = ''
            return

        def get_answer_sql(self):
            return self.answer + Config.sql_extend_answer_filter

    class Epub(object):
        def __init__(self):
            self.article_count = 0
            self.answer_count = 0
            self.agree_count = 0
            self.char_count = 0

            self.title = ''
            self.id = ''
            self.split_index = 0
            self.prefix = ''
            return

    def __init__(self):
        self.kind = ''
        self.author_id = 0
        self.sql = InitialBook.Sql()
        self.epub = InitialBook.Epub()
        self.info = {}
        self.article_list = []
        self.page_list = []
        self.prefix = ''
        return

    def catch_data(self):
        u"""
        从数据库中获取数据
        :return:
        """
        self.catch_info()
        self.get_article_list()  # 获取文章所有信息
        # TODO: __sort
        if self.kind == Type.taoguba_author:
            self.sort_taoguba()
        elif self.kind == Type.xueqiu_author :
            self.sort_xueqiu()
        elif self.kind == Type.sinablog_author:
            self.sort_sina()
        elif  self.kind != Type.csdnblog_author and self.kind != Type.taoguba_author:
            self.__sort()
        return self

    def catch_info(self):
        u"""
        获得博客的信息, 将info作为参数传给set_info
        :return:
        """
        info = {}
        if self.sql.info:
            if self.kind == Type.csdnblog_author:
                info = self.catch_csdnblog_book_info()
            elif self.kind == Type.jianshu_author:
                info = self.catch_jianshu_book_info()
            elif self.kind == Type.sinablog_author:
                info = self.catch_sinablog_book_info()
            elif self.kind == Type.taoguba_author:
                info = self.catch_taoguba_book_info()
            elif self.kind == Type.xueqiu_author:
                info = self.catch_xueqiu_book_info()
            elif self.kind in [Type.question, Type.answer]:
                info = self.catch_question_book_info(self.sql.info)
            elif self.kind == Type.article:
                info = self.catch_article_book_info(self.sql.info)
            else:
                info = DB.cursor.execute(self.sql.info).fetchone()
                info = DB.wrap(Type.info_table[self.kind], info)
        self.set_info(info)
        return

    def catch_csdnblog_book_info(self):
        u"""

        :return:
        """
        info_list = DB.cursor.execute(self.sql.info).fetchall()
        info_list = [DB.wrap(Type.csdnblog_info, item) for item in info_list]
        info = dict()
        info['creator_name'] = '_'.join([str(item['creator_name']) for item in info_list])
        info['creator_id'] = '_'.join([str(item['creator_id']) for item in info_list])
        return info

    def catch_jianshu_book_info(self):
        u"""

        :return: info
        """
        info_list = DB.cursor.execute(self.sql.info).fetchall()
        info_list = [DB.wrap(Type.jianshu_info, item) for item in info_list]
        info = dict()
        # 可以是多个博客组合在一起 TODO: 删掉???
        info['creator_name'] = '_'.join([str(item['creator_name']) for item in info_list])
        info['creator_id'] = '_'.join([str(item['creator_id']) for item in info_list])
        return info

    def catch_sinablog_book_info(self):
        u"""

        :param
        :return: info
        """
        info_list = DB.cursor.execute(self.sql.info).fetchall()
        info_list = [DB.wrap(Type.sinablog_info, item) for item in info_list]
        info = dict()
        info['creator_name'] = '_'.join([str(item['creator_name']) for item in info_list])  # 可以是多个博客组合在一起
        info['creator_id'] = '_'.join([str(item['creator_id']) for item in info_list])
        return info

    def catch_taoguba_book_info(self):
        u"""

        :param
        :return: info
        """
        info_list = DB.cursor.execute(self.sql.info).fetchall()
        info_list = [DB.wrap(Type.taoguba_info, item) for item in info_list]
        info = dict()
        info['creator_name'] = '_'.join([str(item['creator_name']) for item in info_list])  # 可以是多个博客组合在一起
        info['creator_id'] = '_'.join([str(item['creator_id']) for item in info_list])
        return info

    def catch_xueqiu_book_info(self):
        u"""

        :param
        :return: info
        """
        info_list = DB.cursor.execute(self.sql.info).fetchall()
        info_list = [DB.wrap(Type.xueqiu_info, item) for item in info_list]
        info = dict()
        info['creator_name'] = '_'.join([str(item['creator_name']) for item in info_list])  # 可以是多个博客组合在一起
        info['creator_id'] = '_'.join([str(item['creator_id']) for item in info_list])
        return info

    def catch_question_book_info(self, sql):
        info_list = DB.cursor.execute(self.sql.info).fetchall()
        info_list = [DB.wrap(Type.question, item) for item in info_list]
        info = dict()
        info['title'] = '_'.join([str(item['title']) for item in info_list])  # 可以是多个问题, 多个id联系在一起
        info['id'] = '_'.join([str(item['question_id']) for item in info_list])
        return info

    def catch_article_book_info(self, sql):
        info_list = DB.cursor.execute(self.sql.info).fetchall()
        info_list = [DB.wrap(Type.article, item) for item in info_list]
        info = dict()
        info['title'] = '_'.join([str(item['title']) for item in info_list])
        info['id'] = '_'.join([str(item['article_id']) for item in info_list])
        return info

    def set_info(self, info):
        self.info.update(info)
        if self.kind == Type.csdnblog_author:
            self.epub.title = u'csdn博客作者_{}({})文章集锦'.format(info['creator_name'], info['creator_id'])
            self.epub.id = info['creator_id']
        elif self.kind == Type.cnblogs_author:
            self.epub.title = u'cnblogs作者_{}({})文章集锦'.format(info['creator_name'], info['creator_id'])
            self.epub.id = info['creator_id']
        elif self.kind == Type.jianshu_author:  # 该博客所有的博文
            self.epub.title = u'简书作者_{}({})文章集锦'.format(info['creator_name'], info['creator_id'])
            self.epub.id = info['creator_id']
        elif self.kind == Type.jianshu_collection:
            self.epub.title = u'简书专题_{}({})'.format(info['title'], info['collection_fake_id'])
            self.epub.id = info['collection_fake_id']
        elif self.kind == Type.jianshu_notebooks:
            self.epub.title = u'简书文集_{}({})'.format(info['title'], info['notebooks_id'])
            self.epub.id = info['notebooks_id']
        elif self.kind == Type.jianshu_article:  # 单篇博文 TODO
            self.epub.title = u'简书博文集锦({})'.format(info['title'])
            self.epub.id = info['id']  # TODO
        elif self.kind == Type.sinablog_author:  # 该博客所有的博文
            self.epub.title = u'新浪博客_({}){}'.format(info['creator_name'], info['creator_id'])
            self.epub.id = info['creator_id']
        elif self.kind == Type.taoguba_author:  # TGB帖子
            self.epub.title = u'TGB_{}({})'.format(info['creator_name'], info['creator_id'])
            self.epub.id = info['creator_id']
        elif self.kind == Type.xueqiu_author:  # xueqiu
            self.epub.title = u'雪球_{}({})'.format(info['creator_name'], info['creator_id'])
            self.epub.id = info['creator_id']
        elif self.kind == Type.sinablog_article:  # 新浪单篇博文 TODO
            self.epub.title = u'新浪博客博文集锦({})'.format(info['title'])
            self.epub.id = info['id']  # TODO
        elif self.kind == Type.question:
            self.epub.title = u'知乎问题集锦({})'.format(info['title'])
            self.epub.id = info['id']
        elif self.kind == Type.answer:
            self.epub.title = u'知乎回答集锦({})'.format(info['title'])
            self.epub.id = info['id']
        elif self.kind == Type.article:
            self.epub.title = u'知乎专栏文章集锦({})'.format(info['title'])
            self.epub.id = info['id']
        elif self.kind == Type.topic:
            self.epub.title = u'知乎话题_{}({})'.format(info['title'], info['topic_id'])
            self.epub.id = info['topic_id']
        elif self.kind == Type.collection:
            self.epub.title = u'知乎收藏夹_{}({})'.format(info['title'], info['collection_id'])
            self.epub.id = info['collection_id']
        elif self.kind == Type.author:
            self.epub.title = u'知乎作者_{}({})'.format(info['name'], info['author_id'])
            self.epub.id = info['author_id']
        elif self.kind == Type.column:
            self.epub.title = u'知乎专栏_{}({})'.format(info['name'], info['column_id'])
            self.epub.id = info['column_id']
        elif self.kind == Type.yiibai:
            self.epub.title = u'易百教程_{}'.format(info['title'])
            self.epub.id = info['creator_id']
        elif self.kind == Type.talkpython:
            self.epub.title = u'TalkPythonToMe'
            self.epub.id = info['creator_id']

        # from ..html5lib.constants import entities_reverse
        # self.epub.title = Match.replace_words(self.epub.title, entities_reverse)
        return

    def get_article_list(self):
        if self.kind in Type.article_type_list:
            article_list = self.__get_article_list()
        else:
            article_list = self.__get_question_list()
        self.set_article_list(article_list)
        return

    def __get_question_list(self):
        question_list = [DB.wrap('question', x) for x in DB.get_result_list(self.sql.question)]
        answer_list = [DB.wrap('answer', x) for x in DB.get_result_list(self.sql.get_answer_sql())]

        def merge_answer_into_question():
            question_dict = {x['question_id']: {'question': x.copy(), 'answer_list': [], 'agree': 0} for x in
                             question_list}
            for answer in answer_list:
                question_dict[answer['question_id']]['answer_list'].append(answer)
            return question_dict.values()

        def add_property(question):
            agree_count = 0
            char_count = 0
            for answer in question['answer_list']:
                answer['char_count'] = len(answer['content'])
                answer['agree_count'] = answer['agree']
                answer['update_date'] = answer['edit_date']
                agree_count += answer['agree']
                char_count += answer['char_count']
            question['answer_count'] = len(question['answer_list'])
            question['agree_count'] = agree_count
            question['char_count'] = char_count
            return question

        question_list = [add_property(x) for x in merge_answer_into_question() if len(x['answer_list'])]
        return question_list

    def __get_article_list(self):
        def add_property(article):
            article['char_count'] = len(article['content'])
            article['answer_count'] = 1
            # TODO
            if self.kind in [Type.jianshu_author, Type.jianshu_collection, Type.jianshu_notebooks,
                             Type.csdnblog_author, Type.yiibai,]:
                # article['agree_count'] = article['agree']
                print article['agree']
            else:
                article['agree_count'] = article['agree']

            article['update_date'] = article['publish_date']

            return article

        # TODO: 下面的代码可以精简
        if self.kind in [Type.jianshu_author, Type.jianshu_collection, Type.jianshu_notebooks]:
            article_list = [DB.wrap(Type.jianshu_article, x) for x in DB.get_result_list(self.sql.get_answer_sql())]
        elif self.kind == Type.sinablog_author:
            article_list = [DB.wrap(Type.sinablog_article, x) for x in DB.get_result_list(self.sql.get_answer_sql())]
        elif self.kind == Type.taoguba_author:
            article_list = [DB.wrap(Type.taoguba_article, x) for x in DB.get_result_list(self.sql.get_answer_sql())]
        elif self.kind == Type.xueqiu_author:
            article_list = [DB.wrap(Type.xueqiu_article, x) for x in DB.get_result_list(self.sql.get_answer_sql())]
        elif self.kind == Type.csdnblog_author:
            article_list = [DB.wrap(Type.csdnblog_article, x) for x in DB.get_result_list(self.sql.get_answer_sql())]
        elif self.kind == Type.cnblogs_author:
            article_list = [DB.wrap(Type.cnblogs_article, x) for x in DB.get_result_list(self.sql.get_answer_sql())]
        elif self.kind in Type.generic:
            article_list = [DB.wrap(Type.generic_article, x) for x in DB.get_result_list(self.sql.get_answer_sql())]
        else:
            article_list = [DB.wrap(Type.article, x) for x in DB.get_result_list(self.sql.get_answer_sql())]
        article_list = [add_property(x) for x in article_list]
        return article_list

    def set_article_list(self, article_list):
        self.clear_property()
        if self.kind in [Type.jianshu_author, Type.jianshu_collection, Type.jianshu_notebooks,
                         Type.cnblogs_author, Type.sinablog_author, Type.taoguba_author, Type.xueqiu_author,
                         Type.csdnblog_author,
                         Type.yiibai, Type.talkpython]:
            for article in article_list:
                self.epub.answer_count += article['answer_count']
                self.epub.char_count += article['char_count']
        else:  # zhihu类型
            for article in article_list:
                self.epub.answer_count += article['answer_count']
                self.epub.agree_count += article['agree_count']
                self.epub.char_count += article['char_count']
            self.epub.article_count = len(article_list)  # 所以说, 一个question是一个article
        self.article_list = article_list
        return

    def clear_property(self):
        self.epub.answer_count = 0
        self.epub.agree_count = 0
        self.epub.char_count = 0
        self.epub.article_count = 0
        return

    def sort_taoguba(self):
        self.article_list.sort(key=lambda x: (x['author_id'], x[Config.article_order_by], x['title']),
                               reverse=Config.article_order_by_desc)
        return

    def sort_xueqiu(self):
        self.article_list.sort(key=lambda x: (x['publish_date'], x[Config.article_order_by], x['title']),
                               reverse=Config.article_order_by_desc)
        return

    def sort_sina(self):
        self.article_list.sort(key=lambda x: (x['publish_date'], x[Config.article_order_by], x['title']),
                                   reverse= True)
        return

    def __sort(self):
        if self.kind in Type.article_type_list:
            self.sort_article()
        elif self.kind == Type.author:
            self.sort_author_answer()
        else:
            self.sort_question()
        return

    def sort_author_answer(self):
        if Config.author_answer_order_by == 'answer_id':
            self.article_list.sort(key=lambda x: x['answer_list'][0][Config.author_answer_order_by],
                                   reverse=Config.author_answer_order_by_desc)
        else:
            self.article_list.sort(
                key=lambda x: (
                    x['answer_list'][0][Config.author_answer_order_by], x['answer_list'][0]['answer_id']),
                reverse=Config.author_answer_order_by_desc)
        return

    def sort_article(self):
        self.article_list.sort(key=lambda x: (x['author_id'], x[Config.article_order_by], x['title']),
                               reverse=Config.article_order_by_desc)
        return

    def sort_question(self):
        def sort_answer(answer_list):
            answer_list.sort(key=lambda x: x[Config.answer_order_by], reverse=Config.answer_order_by_desc)
            return

        self.article_list.sort(key=lambda x: x[Config.question_order_by], reverse=Config.question_order_by_desc)
        for item in self.article_list:
            sort_answer(item['answer_list'])
        return


class HtmlBookPackage(object):
    def __init__(self):
        self.book_list = []
        self.image_list = []
        self.image_container = ImageContainer()
        return

    def get_title(self):
        title = '_'.join([book.epub.title for book in self.book_list])
        title = Match.fix_filename(title)  # 移除特殊字符
        return title
