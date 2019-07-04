# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from src.lib.wechat_parser.tools.parser_tools import ParserTools
from src.tools.config import Config
from src.tools.match import Match

import re
import time
from collections import OrderedDict
import datetime

class JinWanKanSaEmptColumnParser(ParserTools):
    def __init__(self, content):

        self.dom = BeautifulSoup(content, 'html.parser')

    def get_column_info(self):
        data = {}



        data[u'title'] = ''

        data['image_url'] = ''

        data['article_count'] = 0
        data['follower_count'] = 0
        data['description'] = ''


        return data

class JinWanKanSaColumnParser(ParserTools):
    def __init__(self, content):

        self.dom = BeautifulSoup(content, 'html.parser')

    def get_column_info(self):
        data = {}
        headcontent  = self.dom.find_all('div', class_="header")[0]
        img_src_dict = Match.match_img_with_src_dict(str(headcontent))

        for img in img_src_dict:
            src = img_src_dict[img]
            print src
            data['image_url'] = src

        reInfo = BeautifulSoup(str(headcontent), 'html.parser')
        links = reInfo.findAll('a')
        article_u = (links[1]).text

        description  = self.dom.find_all('span', class_="f12 gray")[0]


        data[u'title'] = article_u

        # data['image_url'] = ''

        data['article_count'] = 0
        data['follower_count'] = 0
        data['description'] = ''


        return data


class JinWanKanSaArticleParser(ParserTools):
    def __init__(self, content):
        self.content = content
        self.dom = BeautifulSoup(content, 'html.parser')

    def get_article_info(self):
        data = {}
        try:
            try:
                title_tationl = self.dom.find_all('h1')
                # print  u"标题 {}".format(span_dom.text.strip()),
                resultstr = title_tationl[0].text


                if resultstr.__contains__('/'):
                    resultstr = Match.replace_specile_chars(resultstr)
                data['title'] = resultstr

                data['title'] = resultstr.strip()

            except IndexError:
                data['title'] = Match.replace_specile_chars(self.dom.title)
            data['title'] = str(data['title']).strip()
            article_body = ""
            istwiterForTurmp = False
            istwiter = False
            if istwiterForTurmp :
                content  = self.dom.find_all('article', class_="weibo-main")[0]
                index_work_sett = OrderedDict()
                #   获取每一页中文章的地址的地址
                for raw_front_page_index in range(0, content.__len__()):
                    index_work_sett[raw_front_page_index] = content[raw_front_page_index]

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
                                tempEn =tempEn + item[1]
                                tempCn =tempCn + item[0]

                            toreplaced = (
                                u"""<div class="Chapter-chapterSpeakerWrapper"> <p data-speaker="" class="">{0}<br/> {1} </p> </div>""".format(
                                        tempEn, tempCn))
                            print ('{}\n{}\n'.format(item[1], item[0]))
                            article_body += str(toreplaced)
                            # transed += ('\n')  # 每段间隔一行


                            del index_work_sett[article_url_index]

                            tempEn = ''
                            tempCn = ''
                            re_catch_counter = 0
                        except Exception as ex:
                            # print('[-]ERROR: ' + str(ex))
                            time.sleep(0.0)
                            re_catch_counter += 1

                            # translate
                data['content'] = str(article_body)
            else:
                if istwiter:
                    content = self.dom.find_all('article', class_="weibo-main")[0]
                else:
                    # 有干扰

                    # content = self.dom.find_all('div', class_="rich_media_content")[0]
                    # print content



                    cc = str(self.content)
                    addss = u"""<script>
    (adsbygoogle = window.adsbygoogle || []).push({});
</script>"""
                    addssds = u"""<span <script="" async="" src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js" style="font-family:宋体;color:#333333;background:white;"></span>"""


                    cc = cc.replace(addss, '', 100)
                    cc = cc.replace(addssds, '', 100)

                    adds = self.dom.find_all('ins', class_="adsbygoogle")
                    addsda = self.dom.find_all('script', async='')
                    for ads in adds:
                        cc = cc.replace(str(adds), '', 1)
                    for ads in addsda:
                        cc = cc.replace(str(adds), '', 1)

                    html_script = r'<div class="rich_media_content" id="js_content">(.*?)</div>'
                    m_script = re.findall(html_script, cc, re.S | re.M)

                    if m_script.__len__() > 0:
                        script = m_script[0]
                        content = str(script)
                    else:

                        content = self.dom.find_all('div', class_="rich_media_content")[0]

                        # id="img-content"



                        # content = self.dom.find_all('div', class_="rich_media_content")[0]

                article_body += str(content)
                data['content'] = str(article_body)

            time_tationl = self.dom.find_all('small', class_="gray")

            tt =  str(time_tationl[0].text)
            ss = tt.split('·')[0]
            ttt = tt.split('·')[-1]

            # print ttt
            rt = str(ttt).strip('\n                    ').strip('\n                ')
            # print rt
            date_time = datetime.datetime.strptime(rt, "%Y-%m-%d %H:%M")
            # print '转化后时间'
            print date_time.strftime('%Y-%m-%d')

            data['updated_time'] = date_time.strftime('%Y-%m-%d')



            # print data['updated_time']
            data['voteup_count'] =  ""
            data['comment_count'] = ""

            data['image_url'] = ''

            data['author_id'] = 'meng-qing-xue-81'


            data['author_name'] = ss
            data['author_headline'] = ''
            data['author_avatar_url'] = 'https://pic4.zhimg.com/v2-38a89e42b40baa7d26d99cab9a451623_xl.jpg'
            data['author_gender'] = '0'
        except Exception as e:
            print e.message
            return []

        return data