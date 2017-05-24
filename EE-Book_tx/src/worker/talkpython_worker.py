#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..tools.http import Http
from ..lib.talkpython_parser.talkpython import TalkPythonParser
from page_worker import PageWorker


__all__ = [
    "TalkPythonWorker"
]


class TalkPythonWorker(PageWorker):
    u"""
    TalkPython worker
    """

    def catch_info(self, target_url):
        if target_url in self.info_url_complete_set:
            return
        content = Http.get_content(target_url)
        if not content:
            return
        self.info_url_complete_set.add(target_url)
        parser = TalkPythonParser(content)

        self.info_list.append(parser.get_extra_info())
        return

    def create_save_config(self):
        config = {
            'generic_article': self.answer_list,
            'generic_info': self.info_list
        }
        return config

    def parse_content(self, content):
        parser = TalkPythonParser(content)
        self.answer_list += parser.get_answer_list()
        pass

    def create_work_set(self, target_url):
        if target_url in self.task_complete_set:
            return

        content = Http.get_content(target_url)
        article_list = TalkPythonParser(content).get_article_list()

        self.task_complete_set.add(target_url)
        for item in article_list:
            self.work_set.add(item)
        return

