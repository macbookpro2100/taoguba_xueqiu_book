# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from src.lib.wechat_parser.tools.parser_tools import ParserTools
from src.tools.match import Match
from src.tools.debug import Debug
import json
import time


class WallStreetcnArticleParser(ParserTools):
    def __init__(self, content):
        # self.dom = BeautifulSoup(content, 'html.parser')

        # strarticle = str(content).replace("\'", '"', 1000)

        self.set_dom(json.dumps(content))
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
            article = json.loads(self.dom)

            data['article_id'] = article['resource']['id']

            title_ = article['resource']['title']

            print  title_

            creatDay = time.strftime("%Y-%m-%d", time.localtime(float(article['resource']['display_time'])))

            title_ = u"{}{}".format(creatDay, title_)
            print title_
            data['title'] = title_
            u"""
            获得博文的内容
            :return:
            """

            article_body = article['resource']['content_text']
            imgs = article['resource']['image_uris']
            for img in imgs:
                print img

                article_body = article_body + u"<img class=\"ke_img\" src=\"{}\" />".format(img)

            # <img class=\"ke_img\" src=\"https://xqimg.imedao.com/16ac34102c7258c3fc2d03de.jpg!custom.jpg\" />

            if not article_body:
                Debug.logger.debug(u"博文内容没有找到")
                article_body = ''
            data['content'] = str(article_body)

            creattime = time.strftime("%Y-%m-%d %H:%M", time.localtime(float(article['resource']['display_time'])))

            # print creattime


            data['updated_time'] = creattime
            data['voteup_count'] = u""
            data['image_url'] = ''
            data['comment_count'] = u""
            data['author_id'] = 'macbookpro2100'

            author_name = ''  # 获得creator_name
            if not author_name:
                Debug.logger.debug(u"没有找到博主姓名")

            data['author_name'] = author_name
            data['author_headline'] = ''
            data['author_avatar_url'] = ''
            data['author_gender'] = '0'

            # if int(article['fav_count']) > 5 or int(article['reply_count']) > 30:
            #     data['author_gender'] = '0'
            # else:
            #     return []

        except Exception as e:
            print e.message
            return []

        return data
