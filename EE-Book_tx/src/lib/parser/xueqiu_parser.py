# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from src.lib.wechat_parser.tools.parser_tools import ParserTools
from src.tools.match import Match
from src.tools.debug import Debug
import json
import time


class XueQiuColumnParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'html.parser')

    def get_column_info(self):
        data = {}
        # find creator_id
        # creator_id = False
        # profile_info_content = self.dom.find_all('div', class_="profile_info_content")
        # try:
        #     for tgo_tgo_ in profile_info_content:
        #         remarks = tgo_tgo_.find_all('a', class_="setRemark")
        #         for remark in remarks:
        #             creator_id = remark.get('data-user-id')
        # except  IndexError as   e:
        #     print e
        #
        # if not creator_id:
        #     Debug.logger.debug(u"没有找到creator_id")



        creator_name = ''
        profile_info_content = self.dom.find_all('div', class_="profile_info_content")
        try:
            for tgo_tgo_ in profile_info_content:
                remarks = tgo_tgo_.find_all('a', class_="setRemark")
                for remark in remarks:
                    creator_name = remark.get('data-user-name')
        except  IndexError as   e:
            print e
        if not creator_name:
            Debug.logger.debug(u"没有找到博主姓名")

        data['title'] = creator_name

        data['article_count'] = 0
        data['follower_count'] = 0
        data['description'] = ''
        data['image_url'] = ''

        return data


class XueQiuArticleParser(ParserTools):
    def __init__(self, content):
        # self.dom = BeautifulSoup(content, 'html.parser')

        # .replace('\'','\"')  .replace('u\"','\"')

        self.set_dom(content)
        # self.dom = content

    def set_dom(self, dom):
        if dom:
            self.dom = dom
        return
    def get_article_info(self):
        data = {}
        try:
            u"""
            获得博文的标题
            :return:
            """
            article = json.loads(self.dom, encoding='utf-8')

            title_ = '回复'
            title_ = article['title']
            if title_.strip() == '':
                title_ = Match.stripTags(article['description'])[0:16]
            if title_.__len__() == 1:
                title_ = '|……'

            data['title'] = title_
            u"""
            获得博文的内容
            :return:
            """

            article_body = article['text']

            if not article_body:
                Debug.logger.debug(u"博文内容没有找到")
                article_body = ''
            data['content'] = str(article_body)
            creattime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(article['created_at'] / 1000)))
            lastedit = creattime if article['edited_at'] == None else time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                    float(article['edited_at'] / 1000)))

            data['updated_time'] = str(lastedit)[:-3]
            data['voteup_count'] = u"收藏:{}".format(article['fav_count'])
            data['image_url'] = ''
            data['comment_count'] = u"评论:{}".format(article['reply_count'])
            data['author_id'] = 'macbookpro2100'

            author_name = article['user']['screen_name']  # 获得creator_name
            if not author_name:
                Debug.logger.debug(u"没有找到博主姓名")

            data['author_name'] = author_name
            data['author_headline'] = ''
            data['author_avatar_url'] = ''
            data['author_gender'] = '0'
        except Exception as e:
            print e.message
            return []

        return data
