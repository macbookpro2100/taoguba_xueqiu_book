# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from src.lib.wechat_parser.tools.parser_tools import ParserTools
from src.tools.config import Config
from src.tools.match import Match

from src.lib.googlet.translate import translate
import time
from collections import OrderedDict


class BuffettColumnParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'html.parser')

    def get_column_info(self):
        data = {}

        data['article_count'] = 0
        data['follower_count'] = 0
        data['description'] = ''
        data['image_url'] = ''

        return data


class BuffettArticleParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'lxml')
    # 解析+翻译
    def parse_answer_content(self):

        article_body = ""

        list_tiezhi_0 = self.dom.find_all('p', class_="Buffett-clipVideoHeroHeaderDescription")[0]

        # 一条线

        line = (u"""
                <div>
                <br />
                <hr style=" height:2px;border:none;border-top:2px dotted #185598;" />
                <br />
                </div>
            """)

        content = self.dom.find_all('div', class_="Transcript-transcriptChaptersWrapper")[0]

        list_text = \
            content.find_all('div', class_="Transcript-transcriptStickyVideoWrapper Transcript-transcriptBackToTop")[0]

        listssSyncVideotoParagraph = content.find_all('div', class_="ChapterParagraph-chapterParagraphToolTipText")[0]

        content = (str(content)).replace(str(list_text), '', 2)
        content = (str(content)).replace(str(listssSyncVideotoParagraph), '', 999999)

        article_body += str(list_tiezhi_0)
        article_body += str(line)
        article_body += str(content)

        xxsoup = BeautifulSoup(article_body, 'lxml')

        list_tiezhi_tit = xxsoup.find_all('div', class_="Chapter-chapterTitle")

        index_work_seth = OrderedDict()
        #   获取每一页中文章的地址的地址
        for raw_front_page_index in range(0, list_tiezhi_tit.__len__()):
            index_work_seth[raw_front_page_index] = list_tiezhi_tit[raw_front_page_index]

        re_catch_counter = 0
        while len(index_work_seth) > 0 and re_catch_counter <= 20:
            re_catch_counter += 1
            for article_url_index in index_work_seth:
                ll = index_work_seth[article_url_index]
                tll = ll.text
                try:
                    ret = translate(tll)
                    tempEn = ''
                    tempCn = ''
                    if not ret:
                        raise Exception('Empty Response')
                    for item in ret:
                        tempEn = tempEn + item[1]
                        tempCn = tempCn + item[0]
                    toreplaced = (
                        u"""<div class="Buffett-clipVideoHeroHeaderDescription"> <p data-speaker="" class=""> {0}<br/> {1} </p> </div>""".format(
                            item[1], item[0]))
                    print ('{}\n{}\n'.format(item[1], item[0]))
                    article_body = str(article_body).replace(str(ll), toreplaced, 1)
                    # transed += ('\n')  # 每段间隔一行
                    del index_work_seth[article_url_index]
                    tempEn = ''
                    tempCn = ''
                    re_catch_counter = 0
                except Exception as ex:
                    # print('[-]ERROR: ' + str(ex))
                    time.sleep(0.0)
                    re_catch_counter += 1

        list_tiezhi_tit = xxsoup.find_all('div', class_="Chapter-chapterTitle")

        index_work_sett = OrderedDict()
        #   获取每一页中文章的地址的地址
        for raw_front_page_index in range(0, list_tiezhi_tit.__len__()):
            index_work_sett[raw_front_page_index] = list_tiezhi_tit[raw_front_page_index]

        re_catch_counter = 0
        while len(index_work_sett) > 0 and re_catch_counter <= 20:
            re_catch_counter += 1
            for article_url_index in index_work_sett:
                ll = index_work_sett[article_url_index]
                tll = ll.text
                try:
                    ret = translate(tll)
                    tempEn = ''
                    tempCn = ''

                    if not ret:
                        raise Exception('Empty Response')
                    for item in ret:
                        tempEn = tempEn + item[1]
                        tempCn = tempCn + item[0]

                    toreplaced = (
                        u"""<div class="Chapter-chapterSpeakerWrapper"> <p data-speaker="" class=""><b><font size="2" color="#56A5EC"> {0}<br/> {1} </font></b></p> </div>""".format(
                            tempEn, tempCn))
                    print ('{}\n{}\n'.format(item[1], item[0]))
                    article_body = str(article_body).replace(str(ll), toreplaced, 1)
                    # transed += ('\n')  # 每段间隔一行
                    del index_work_sett[article_url_index]

                    tempEn = ''
                    tempCn = ''
                    re_catch_counter = 0
                except Exception as ex:
                    # print('[-]ERROR: ' + str(ex))
                    time.sleep(0.0)
                    re_catch_counter += 1

        toTrans = xxsoup.find_all('div', class_="Chapter-chapterSpeakerWrapper")

        index_work_set = OrderedDict()
        #   获取每一页中文章的地址的地址
        for raw_front_page_index in range(0, toTrans.__len__()):
            index_work_set[raw_front_page_index] = toTrans[raw_front_page_index]

        re_catch_counter = 0
        while len(index_work_set) > 0 and re_catch_counter <= 20:
            re_catch_counter += 1
            for article_url_index in index_work_set:
                ll = index_work_set[article_url_index]
                tll = ll.text
                try:
                    ret = translate(tll)
                    tempEn = ''
                    tempCn = ''

                    if not ret:
                        raise Exception('Empty Response')
                    for item in ret:
                        tempEn = tempEn + item[1]
                        tempCn = tempCn + item[0]

                    toreplaced = (
                        u"""<div class="Chapter-chapterSpeakerWrapper"> <p data-speaker="" class="">{0}<br/> {1} </p> </div>""".format(
                            tempEn, tempCn))
                    print ('{}\n{}\n'.format(item[1], item[0]))
                    article_body = str(article_body).replace(str(ll), toreplaced, 1)
                    # transed += ('\n')  # 每段间隔一行
                    del index_work_set[article_url_index]

                    tempEn = ''
                    tempCn = ''
                    re_catch_counter = 0
                except Exception as ex:
                    # print('[-]ERROR: ' + str(ex))
                    time.sleep(0.0)
                    re_catch_counter += 1

        return article_body

    def get_article_info(self):
        data = {}
        try:
            try:
                title_tationl = self.dom.find_all('h2', class_="Buffett-clipVideoHeroHeaderTitle")
                # print  u"标题 {}".format(span_dom.text.strip()),
                resultstr = title_tationl[0].text

                if resultstr.__contains__('/'):
                    resultstr = Match.replace_specile_chars(resultstr)

                data['title'] = resultstr.strip()

            except IndexError:
                data['title'] = Match.replace_specile_chars(self.dom.title)
            data['title'] = str(data['title']).strip()

            data['content'] = str(self.parse_answer_content())

            time_tationl = self.dom.find_all('div', class_="Buffett-clipVideoHeroHeaderTimestamp")

            tt = time_tationl[0].text

            print tt[:-4]

            # print  sp[0].text + ' '+sp[1].text+'  '+sp[2].text

            data['updated_time'] = tt[:-4]

            # print data['updated_time']
            data['voteup_count'] = ""
            data['comment_count'] = ""

            data['image_url'] = ''

            data['author_id'] = 'meng-qing-xue-81'

            data['author_name'] = 'CNBC'
            data['author_headline'] = ''
            data['author_avatar_url'] = 'https://pic4.zhimg.com/v2-38a89e42b40baa7d26d99cab9a451623_xl.jpg'
            data['author_gender'] = '0'
        except Exception as e:
            print e.message
            return []

        return data
