#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from ..tools.TGBHttp import Http
from ..tools.match import Match

from taoguba_base_worker import TGPageWorker
from ..lib.taoguba_parser.taoguba_parser import TGBParser

from ..lib.parser_tools import ParserTools

__all__ = [
    "taogubaAuthorWorker",
]


class taogubaAuthorWorker(TGPageWorker):
    def create_save_config(self):
        config = {'taoguba_article': self.answer_list, 'taoguba_info': self.question_list}
        return config

    def parse_content(self, content):
        parser = TGBParser(content)
        self.answer_list += parser.get_answer_list()

    def create_work_set(self, target_url):
        u"""

        :param target_url: http://blog.csdn.net/dbzhang800
        :return:
        """
        if target_url in self.task_complete_set:
            return
        id_result = Match.taoguba_article(target_url)
        tgb_article_id = id_result.group('article_id')
        tgb_range_id = int(id_result.group('range_id'))
        self.task_complete_set.add(target_url)

        page0 = 'http://www.taoguba.com.cn/Article/' + tgb_article_id + '/1'

        content_profile = Http.get_content(page0)
        parser = TGBParser(content_profile)
        self.question_list += parser.get_extra_info()
        if tgb_range_id == 0:
            dom = BeautifulSoup(content_profile, "lxml")
            list_pcyc_l_ = dom.find_all('div', class_="left t_page01")
            try:
                for tgo_tgo_ in list_pcyc_l_:
                    linkl = tgo_tgo_.findAll('a')
                    tarUrl = linkl[0].get('href')
                    tgb_range_id = int(tarUrl.split('/')[3])

            except  IndexError as   e:
                tgb_range_id = 1

        #

        for indx in range(1, int(tgb_range_id) + 1):
            url = 'http://www.taoguba.com.cn/Article/' + tgb_article_id + '/' + str(indx)
            self.work_set.add(url)
        return
