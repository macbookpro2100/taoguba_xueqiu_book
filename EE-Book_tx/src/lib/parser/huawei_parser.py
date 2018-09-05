# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from src.lib.wechat_parser.tools.parser_tools import ParserTools
from src.tools.match import Match

class HuaWeiColumnParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'html.parser')

    def get_column_info(self):
        data = {}

        data['article_count'] = 0
        data['follower_count'] = 0
        data['description'] = ''
        data['image_url'] = ''

        return data


class HuaWeiArticleParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'lxml')

    def get_article_info(self):
        data = {}
        try:
            try:

                list_articl_info = self.dom.find_all('div', class_="bbs_info_right_title")[0]
                # do fix
                span_dom = list_articl_info.find_all('label', id="topicTitle")[0]

                # print  u"标题 {}".format(span_dom.text.strip()),
                resultstr = span_dom.text.strip()

                resulttitle = ''

                if resultstr.__len__() > 0:

                    resulttitle = resultstr
                else:
                    resulttitle = list_articl_info.text.strip()

                if resulttitle.__contains__('/'):
                    title = Match.replace_specile_chars(resulttitle)
                    data['title'] = title
                else:
                    data['title'] = resulttitle

            except IndexError:
                data['title'] = Match.replace_specile_chars(self.dom.title)
            data['title'] = str(data['title']).strip()
            article_body = ""

            list_tiezhi_0 = self.dom.find_all('div', class_="bbs_info_right_text")[0]



            retEmptyline = []
            headNouse_dom = list_tiezhi_0.find_all('p',align="center")


            for d in headNouse_dom[:3]:
                if str(d.text).__len__() == 0 and not str(d).__contains__('jpg'):
                    retEmptyline.append(str(d))

            ret = ''
            realtt = ''
            headBigTitle_dom = list_tiezhi_0.find_all('p')
            headf = headBigTitle_dom[:6]
            for x in headf :
                xx = str(x.text).strip().replace(' ', '')
                if xx.__contains__('总裁') :
                    print str(xx)
                    ret = str(x)
                if xx.strip().__contains__('签发') :
                    if str(xx).split('【') > 1:
                        print str(xx).split('【')[-1]
                        data['author_name'] = (u'【{}'.format(str(xx).split('【')[-1])).replace('          ', ' ',1)
                    else :
                        data['author_name'] = str(xx)
                    realtt = str(x)

            for em in retEmptyline :
                print em
                list_tiezhi_0 = str(list_tiezhi_0).replace(em,'',1)
            if ret.__len__() >1 :
                list_tiezhi_0 = str(list_tiezhi_0).replace(ret,'',1)
            if realtt.__len__() >1 :
                list_tiezhi_0 = str(list_tiezhi_0).replace(realtt,'',1)

            article_body += str(list_tiezhi_0)
            # print str(tgo)

            data['content'] = str(article_body)

            time_dom = self.dom.find_all('div', class_="bbs_info_right_pro")[0]
            sp = time_dom.find_all('span', class_="fl")

            # print  sp[0].text + ' '+sp[1].text+'  '+sp[2].text

            data['voteup_count'] = u"评论:{}".format(sp[3].text)
            data['comment_count'] = u" 浏览:{}".format(sp[2].text)

            timestr = str(Match.replace_stimespecile_chars((sp[0]).text))
            tt = timestr[0:10] + ' ' + timestr[10:]



            data['updated_time'] = tt


            data['image_url'] = ''

            data['author_id'] = 'meng-qing-xue-81'

            data['author_headline'] = ''
            data['author_avatar_url'] = 'https://pic4.zhimg.com/v2-38a89e42b40baa7d26d99cab9a451623_xl.jpg'
            data['author_gender'] = '0'
        except Exception as e:
            print e.message
            return []

        return data