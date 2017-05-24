# -*- coding: utf-8 -*-
import sqlite3


from tools.path import Path
from book import Book
from tools.config import Config
from tools.debug import Debug
from tools.db import DB
from login import Login
from url_parser import UrlParser
from worker import worker_factory
from utils import log


class EEBook(object):
    def __init__(self, recipe_kind='Notset', read_list='ReadList.txt', url=None, debug=False):
        u"""
        配置文件使用$符区隔，同一行内的配置文件归并至一本电子书内
        :param recipe_kind:
        :param read_list: default value: ReadList.txt
        :param url:
        :param debug:
        :return:
        """
        self.recipe_kind = recipe_kind
        self.read_list = read_list
        self.url = url
        log.warning_log(u"website type: " + str(self.recipe_kind) + '\n')
        import logging
        if debug is True:
            Debug.logger.setLevel(logging.DEBUG)
        else:
            Debug.logger.setLevel(logging.INFO)

        Debug.logger.debug(u"read_list: " + str(self.read_list))
        Debug.logger.debug(u"url: " + str(self.url))
        Debug.logger.debug(u"recipe type:" + str(recipe_kind))

        Path.init_base_path(recipe_kind)        # 设置路径
        Path.init_work_directory()              # 创建路径
        self.init_database()                    # 初始化数据库
        Config._load()
        return

    @staticmethod
    def init_config(recipe_kind):
        if recipe_kind == 'zhihu':      # TODO: 再有一个需要登录的网站, 改掉硬编码
            login = Login(recipe_kind='zhihu')
        else:
            return
        # !!!!!发布的时候把Config.remember_account改成false!!!!!,第一次需要登录,之后用cookie即可
        # 登陆成功了,自动记录账户
        if Config.remember_account_set:
            Debug.logger.info(u'Detected settings file，use it.')
            Config.picture_quality = 1
        else:
            log.warning_log(u"Please login...")
            login.start()
            Config.picture_quality = 1
            Config.remember_account_set = True
        Config._save()
        return

    def begin(self):
        u"""
        程序运行的主函数
        :return: book file 的列表
        """
        Debug.logger.debug(u"#DEBUG MODE#: don't check update")
        self.init_config(recipe_kind=self.recipe_kind)
        if self.url is None:
            Debug.logger.debug(u"Reading ReadList.txt...")
        else:
            Debug.logger.debug(u"Got url: " + str(self.url))
        book_files = []
        if self.url is not None:
            file_name = self.create_book(self.url, 1)
            book_files.append(file_name)
            return book_files

        counter = 1
        try:
            with open(self.read_list, 'r') as read_list:
                for line in read_list:
                    line = line.replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')  # 移除空白字符
                    file_name = self.create_book(line, counter)
                    book_files.append(file_name)
                    counter += 1
        except IOError as e:
            Debug.logger.debug(u"\nCreating " + self.read_list + "...")
            with open(self.read_list, 'w') as read_list:
                read_list.close()
        if 1 == counter:
            print(u"\nOops! No content in " + self.read_list + ". Please check it out.")
            return
        return book_files

    @staticmethod
    def create_book(command, counter):
        Path.reset_path()

        Debug.logger.info(u"Ready to make No.{} e-book".format(counter))
        Debug.logger.info(u"Analyzes {} ".format(command))
        task_package = UrlParser.get_task(command)  # 分析命令
        if not task_package.is_work_list_empty():
            worker_factory(task_package.work_list)  # 执行抓取程序
            Debug.logger.info(u"Complete fetching from web")

        file_name_set = None
        if not task_package.is_book_list_empty():
            Debug.logger.info(u"Start generating e-book from the database")
            book = Book(task_package.book_list)
            file_name_set = book.create()
        if file_name_set is not None:
            file_name_set2list = list(file_name_set)
            file_name = '-'.join(file_name_set2list[0:3])
            return file_name
        return u"Oops! no epub file produced"

    @staticmethod
    def init_database():
        if Path.is_file(Path.db_path):
            Debug.logger.debug(u"Connect to the database...")
            Debug.logger.debug(u"db_path: " + str(Path.db_path))
            DB.set_conn(sqlite3.connect(Path.db_path))
        else:
            Debug.logger.debug(u"Create db file...")
            DB.set_conn(sqlite3.connect(Path.db_path))
            with open(Path.sql_path) as sql_script:
                DB.cursor.executescript(sql_script.read())
            DB.commit()
