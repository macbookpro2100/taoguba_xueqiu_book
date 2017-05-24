# -*- coding: utf-8 -*-
import re

from ...parser_tools import ParserTools
from ....tools.match import Match
from ....tools.debug import Debug
from bs4 import BeautifulSoup
import urllib
from ....tools.config import Config


def getPostTimeString(text):
    str_all = "".join(text.split())
    str_author_time = str_all[:-10]
    str_time = str_author_time[-15:]
    str_author = str_author_time[:-15]
    str_day = str_time[:10]
    str_hour = str_time[10:]
    return str_author + " " + str_day + " " + str_hour + '】'


class TGBArticle(ParserTools):
    def __init__(self, dom=None):
        self.set_dom(dom)
        self.info = {}

        return

    def set_dom(self, dom):
        if dom:
            self.dom = dom
        return

    def get_info(self):
        answer_info = self.parse_info()
        return answer_info

    def parse_info(self):
        self.parse_author_id()
        self.parse_author_name()
        self.parse_article_id()
        self.parse_article_title()
        self.parse_answer_content()  # 获得博文的内容
        # self.parse_href()
        # self.parse_comment()          # TODO
        # self.parse_publish_data()     # TODO
        return self.info

    def parse_answer_content(self):
        u"""
        获得博文的内容
        :return:
        """
        article_body = ''

        article_index = self.getArticleIndex()  # 第一页
        if article_index == '1' or article_index == '01' or article_index == '001' or article_index == '0001':
            list_tiezhi_0 = self.dom.find_all('div', class_="p_wenz")
            for tgo in list_tiezhi_0:
                maincontext = ''
                bouttomStr = ''
                # 保留主内容
                list_coten = tgo.find_all('div', class_="p_coten")
                for tgo_right in list_coten:
                    maincontext = str(tgo_right)
                list_p_title = tgo.find_all('div', class_="p_title")
                for p_title in list_p_title:
                    # print "".join(p_title.text.split())[:-10]
                    bouttomStr = p_title.text
                    p_title.clear()
                article_body += (u"""
               <div class="answer-body">
                    <div class="answer-content">
                          {0}
                        <br/>
                    </div>
                    <div    class='zm-item-comment-el'>
                        <div  class='update' >
                            {1}<font size="2" color="grey">{2}</font>
                        </div>
                    </div>
               </div>
               <hr/>""".format(maincontext, "", bouttomStr))




            #      捧场   点亮
            pengchangreply_context_list = []
            # 捧场
            pengchangreply = self.dom.find_all('div', id="pengchangreply")
            for x in pengchangreply:
                pengchangreply_list = x.find_all('div', class_="pc_p_nr")
                for tt in pengchangreply_list:
                    if not pengchangreply_context_list.__contains__(tt):
                        pengchangreply_context_list.append(tt)

            # 点亮
            lightenreply_context_list = []
            lightenreply = self.dom.find_all('div', id="lightenreply")
            for x in lightenreply:
                lightenreply_list = x.find_all('div', class_="pc_p_nr")
                for tt in lightenreply_list:
                    if not pengchangreply_context_list.__contains__(tt):
                        lightenreply_context_list.append(tt)

            for tgo in pengchangreply_context_list:
                maincontext = ''
                bouttomStr = ''
                # 保留主内容
                list_coten = tgo.find_all('div', class_="pcnr_wz")
                for tgo_right in list_coten:
                    maincontext = str(tgo_right)
                list_pcyc_l_ = tgo.find_all('div', class_="left pcyc_l")
                for tgo_tgo_ in list_pcyc_l_:
                    # print "".join(tgo_tgo_.text.split())[:-10]
                    bouttomStr = getPostTimeString(tgo_tgo_.text)
                    tgo_tgo_.clear()
                article_body += (u"""
               <div class="answer-body">
                    <div class="answer-content">
                          {0}
                        <br/>
                    </div>
                    <div    class='zm-item-comment-el'>
                        <div  class='update' >
                            {1}<font size="2" color="#56A5EC">{2}</font>
                        </div>
                    </div>
               </div>
               <hr/>""".format(maincontext, "", bouttomStr))

            for tgo in lightenreply_context_list:
                maincontext = ''
                bouttomStr = ''
                # 保留主内容
                list_coten = tgo.find_all('div', class_="pcnr_wz")
                for tgo_right in list_coten:
                    maincontext = str(tgo_right)
                list_pcyc_l_ = tgo.find_all('div', class_="left pcyc_l")
                for tgo_tgo_ in list_pcyc_l_:
                    # print "".join(tgo_tgo_.text.split())[:-10]
                    bouttomStr = getPostTimeString(tgo_tgo_.text)
                    tgo_tgo_.clear()
                article_body += (u"""
               <div class="answer-body">
                    <div class="answer-content">
                          {0}
                        <br/>
                    </div>
                    <div    class='zm-item-comment-el'>
                        <div  class='update' >
                            {1}<font size="2" color="#0000FF">{2}</font>
                        </div>
                    </div>
               </div>
               <hr/>""".format(maincontext, "", bouttomStr))


        list_tationl = self.dom.find_all('div', class_="p_tationl")
        for tgo_tationl in list_tationl:
            # 解析 时间 阅读 赞同
            # print tgo_tationl

            totalViewNum = tgo_tationl.find_all('span', id="totalViewNum")[0]
            replyNum = tgo_tationl.find_all('span', id="replyNum")[0]
            lastdtit = tgo_tationl.find_all('span', class_="p_tatime")[0]
            self.info['comment'] = u"阅读:{}".format(totalViewNum.text)
            self.info['agree'] = u"回复:{}".format(replyNum.text)

            print lastdtit.text

            self.info['publish_date'] = lastdtit.text
        # 抓取 作者还是全部
        # cals = "pc_p_nr"
        cals = u"pc_p_nr user_{}".format(Config.now_id)
        list_tiezhi_1 = self.dom.find_all('div', class_=cals)

        for tgo in list_tiezhi_1:
            bouttomStr = ''
            # 保留主内容
            list_text = tgo.find_all('div', class_="pcpnr_bt right")
            for tgo_right in list_text:
                tgo_right.clear()

            list_text_fot = tgo.find_all('div', class_="pcnr_fot")
            for tgo_fot in list_text_fot:
                tgo_fot.clear()

            list_tgo_tgo_ = tgo.find_all('div', class_="tgo_")
            for p_title in list_tgo_tgo_:
                p_title.clear()

            list_p_title = tgo.find_all('div', class_="left pcyc_l")
            for p_title in list_p_title:
                # print "".join(tgo_tgo_.text.split())[:-10]
                bouttomStr = getPostTimeString(p_title.text)
                p_title.clear()

            article_body += (u"""
               <div class="answer-body">
                    <div class="answer-content">
                          {0}
                        <br/>
                    </div>
                    <div    class='zm-item-comment-el'>
                        <div  class='update' >
                            {1}<font size="2" color="grey">{2}</font>
                        </div>
                    </div>
               </div>
               <hr/>""".format(tgo, "", bouttomStr))

        if not article_body:
            Debug.logger.debug(u"博文内容没有找到")
            return
        article_body = str(article_body)
        self.info['content'] = article_body

    def parse_author_id(self):
        u"""
        获得author_id
        :return:
        """
        article_id = ''

        list_pcyc_l_ = self.dom.find_all('div', class_="p_title")
        for tgo_tgo_ in list_pcyc_l_:
            for link in tgo_tgo_.findAll('a'):
                article_id = str(link.get('href')).split('/')[1]
        self.info['author_id'] = article_id

    def parse_author_name(self):
        u"""
        获得author的姓名
        :return:

        """
        article_title = ''
        article_id = ''

        list_pcyc_l_ = self.dom.find_all('div', class_="p_title")
        for tgo_tgo_ in list_pcyc_l_:
            for link in tgo_tgo_.findAll('a'):
                article_id = str(link.get('href')).split('/')[1]
            article_title = Match.fix_filename(tgo_tgo_.text)
        self.info['author_name'] = article_title

    def parse_article_id(self):
        u"""
        获得博文的id
        :return:
        """

        article_title = ''
        article_id = ''
        article_index = ''
        # article_id should index page
        list_pcyc_l_ = self.dom.find_all('div', class_="p_title")
        for tgo_tgo_ in list_pcyc_l_:
            for link in tgo_tgo_.findAll('a'):
                article_id = str(link.get('href')).split('/')[1]
        article_index = self.getArticleIndex()

        Debug.logger.debug(article_index)
        self.info['article_id'] = article_id + '_' + str(article_index)

    def getArticleIndex(self):
        maxPage = 1
        list_pcyc_l_ = self.dom.find_all('div', class_="left t_page01")
        try:
            for tgo_tgo_ in list_pcyc_l_:
                linkl = tgo_tgo_.findAll('a')
                tarUrl = linkl[0].get('href')
                maxPage = int(tarUrl.split('/')[3])

        except  IndexError as   e:
            maxPage = 1
        # 不足位补0
        formatType = "{:0>1d}"
        if maxPage > 10:
            if maxPage > 10 and maxPage < 100:
                formatType = "{:0>2d}"
            elif maxPage > 100 and maxPage < 1000:
                formatType = "{:0>3d}"
            else:
                formatType = "{:0>4d}"
        article_index = 1
        try:
            list_fot = self.dom.find_all('div', class_="left t_page01")
            for item in re.findall(r'\<span>.*?\</span\>', str(list_fot[0])):
                find = re.search(r'(?<=;"\>)(?P<id_id>[^/\n\r]*)(</b\>)', str(item))
                article_index = find.group('id_id')
        except  IndexError as   e:
            return article_index
        if article_index == 1:
            return ''
        else:
            return formatType.format(int(article_index))

    def parse_article_title(self):
        u"""
        获得博文的标题
        :return:
        """

        article_title = ''
        article_id = ''

        list_pcyc_l_ = self.dom.find_all('div', class_="p_title")
        for tgo_tgo_ in list_pcyc_l_:
            for link in tgo_tgo_.findAll('a'):
                article_id = str(link.get('href')).split('/')[1]
            article_title = Match.fix_filename(tgo_tgo_.text)
        # article_title +

        self.info['title'] = article_title + str(self.getArticleIndex())
