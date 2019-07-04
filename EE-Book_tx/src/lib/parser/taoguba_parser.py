# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from src.lib.wechat_parser.tools.parser_tools import ParserTools
from src.tools.config import Config
from src.tools.match import Match
import datetime
import re
import time
import re


class TaoGuBaColumnParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'html.parser')

    def get_column_info(self):
        data = {}

        article_title = ''
        article_id = ''

        list_pcyc_l_ = self.dom.find_all('div', class_="p_title")
        for tgo_tgo_ in list_pcyc_l_:
            for link in tgo_tgo_.findAll('a'):
                article_id = str(link.get('href')).split('/')[1]
                article_title = tgo_tgo_.text.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')

        data['column_id'] = article_id
        data['title'] = article_title
        data['article_count'] = 0
        data['follower_count'] = 0
        data['description'] = ''
        data['image_url'] = ''

        print article_id + '         ' + article_title

        return data


def getPostTimeString(text):
    str_all = "".join(text.split())
    str_author_time = str_all[:-10]
    str_time = str_author_time[-15:]
    str_author = str_author_time[:-15]
    str_day = str_time[:10]
    str_hour = str_time[10:]
    return str_author + " " + str_day + " " + str_hour + '】'


def taogubaImgClass(content=''):
    u"""
    :param content: <img class="lazy" data-original="http://image.taoguba.com.cn/img/2016/04/19/wq3fb28kcslb.png@!topic" data-type="contentImage" onclick="self.open(this.src);" onload="javascript:if(this.width&gt;760)this.width=760" src="placeHolder.png"/>
    :return:     http://image.taoguba.com.cn/img/2016/04/19/wq3fb28kcslb.png@!topic
    """
    re_type = r'data-original="([^\"]+?\@!topic)" data-type='
    imgre = re.compile(re_type)
    images = re.findall(imgre, content)
    # print images
    return images[0]


def fixLazyImg(content):
    tgo = BeautifulSoup(content, 'lxml')
    list_img_context = tgo.find_all('div', align="center")
    for img_context in list_img_context:
        list_img_ = img_context.find_all('img', class_="lazy")
        for img in list_img_:
            # print(img)
            try:
                img_http = taogubaImgClass(str(img))
                # print img_http
                # filename = self.image_container.add(img_http)
                # filename = self.image_container.add(src_download)
                # img_file_path = imgfolder + '/' + img_http.split('/')[-1]
                # urllib.urlretrieve(img_http, img_file_path, cbk)
                # print   img_http.split('/')[-1]

                tarImg = '<img class="ke_img" src="' + img_http + '" >'
                img_context.clear()
                extraSoup = BeautifulSoup(u'{}'.format(tarImg))
                img_context.insert(0, extraSoup)
            except  IndexError as   e:
                continue
            except  AttributeError as   e:
                continue
    return str(tgo)


# 帖子 解析
class TaoGuBaParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'lxml')

    def parse_author_id(self):
        u"""
        获得author_id
        :return:
        """
        author_id = ''
        list_pcyc_l_ = self.dom.find_all('div', class_="p_tationl")[0]

        link = list_pcyc_l_.findAll('a')[0]

        author_ids = str(link.get('href')).split('/')[-1]

        # print  "parse_author_id + "+ author_ids

        author_id = author_ids
        return author_id

    def parse_creator_name(self):
        u"""
        "关于我"页面上, ownernick的内容
        :return:
        """
        article_title = ''
        article_id = ''

        list_pcyc_l_ = self.dom.find_all('div', class_="p_tationl")[0]

        link = list_pcyc_l_.findAll('a')[0]
        # print link

        article_title = link.text.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')

        # print article_title


        return article_title

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

        return article_id + '_' + str(article_index)

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

        return article_title + str(self.getArticleIndex()).strip()

    def get_article_info(self):
        data = {}
        try:

            data['title'] = self.parse_article_title()

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

                        </div>
                        <div    class='zm-item-comment-el'>
                            <div  class='update' >
                                {1}<font size="2" color="grey">{2}</font>
                            </div>
                        </div>
                   </div>
                   <hr/>""".format(maincontext, "", bouttomStr))

                # 捧场   点亮
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
                data['comment_count'] = u"阅读:{}".format(totalViewNum.text)
                data['voteup_count'] = u"回复:{}".format(replyNum.text)

                date_time = datetime.datetime.strptime(str(lastdtit.text).strip(), "%Y-%m-%d %H:%M")
                print '转化后时间 ' + date_time.strftime("%Y-%m-%d %H:%M")

                data['updated_time'] = date_time.strftime("%Y-%m-%d %H:%M")
            # 抓取 作者还是全部
            # cals = "pc_p_nr"
            cals = u"pc_p_nr user_{}".format(self.parse_author_id())
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

                        </div>
                        <div    class='zm-item-comment-el'>
                            <div  class='update' >
                                {1}<font size="2" color="grey">{2}</font>
                            </div>
                        </div>
                   </div>
                   <hr/>""".format(tgo, "", bouttomStr))

            if not article_body:
                print u"作者 {} 没有跟帖 {}".format(self.parse_creator_name(), self.parse_article_id())
                return []

            # fix img lazy load


            data['content'] = fixLazyImg(str(article_body))
            data['image_url'] = ''
            data['author_id'] = 'meng-qing-xue-81'
            data['author_name'] = self.parse_creator_name()
            data['author_headline'] = ''
            data['author_avatar_url'] = 'https://pic4.zhimg.com/v2-38a89e42b40baa7d26d99cab9a451623_xl.jpg'
            data['author_gender'] = '0'
        except Exception as e:
            print e.message
            return []

        return data


# 文章集 解析


class TaoGuBaAllParser(ParserTools):
    def __init__(self, content, account_id):
        self.dom = BeautifulSoup(content, 'lxml')
        self.account_id = account_id

    def parse_author_id(self):
        u"""
        获得author_id
        :return:
        """
        author_id = ''
        list_pcyc_l_ = self.dom.find_all('div', class_="p_tationl")[0]

        link = list_pcyc_l_.findAll('a')[0]

        author_ids = str(link.get('href')).split('/')[-1]

        # print  "parse_author_id + "+ author_ids

        author_id = author_ids
        return author_id

    def parse_creator_name(self):
        u"""
        "关于我"页面上, ownernick的内容
        :return:
        """
        article_title = ''
        article_id = ''

        list_pcyc_l_ = self.dom.find_all('div', class_="p_tationl")[0]

        link = list_pcyc_l_.findAll('a')[0]
        # print link

        article_title = link.text.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')

        # print article_title

        return article_title

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

        return article_id

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

        if self.parse_author_id() != self.account_id:
            article_title = u"跟帖:{}".format(article_title.strip())

        return article_title.strip()

    def get_article_info(self):
        data = {}
        try:

            data['title'] = self.parse_article_title()

            u"""
            获得博文的内容
            :return:
            """
            article_body = ''

            article_index = '1'  # 第一页
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

                        </div>
                        <div    class='zm-item-comment-el'>
                            <div  class='update' >
                                {1}<font size="2" color="grey">{2}</font>
                            </div>
                        </div>
                   </div>
                   <hr/>""".format(maincontext, "", bouttomStr))

                # 捧场   点亮
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


                #
                pengchangreply_context_list = []
                # 点亮
                lightenreply_context_list = []

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
                data['comment_count'] = u"阅读:{}".format(totalViewNum.text)
                data['voteup_count'] = u"回复:{}".format(replyNum.text)

                date_time = datetime.datetime.strptime(str(lastdtit.text).strip(), "%Y-%m-%d %H:%M")
                print '转化后时间 ' + date_time.strftime("%Y-%m-%d %H:%M")

                data['updated_time'] = date_time.strftime("%Y-%m-%d %H:%M")
            # 抓取 作者还是全部
            # cals = "pc_p_nr"
            cals = u"pc_p_nr user_{}".format(self.account_id)
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
                        </div>
                        <div    class='zm-item-comment-el'>
                            <div  class='update' >
                                {1}<font size="2" color="grey">{2}</font>
                            </div>
                        </div>
                   </div>
                   <hr/>""".format(tgo, "", bouttomStr))

            if not article_body:
                print u"作者 {} 没有跟帖 {}".format(self.parse_creator_name(), self.parse_article_id())
                return []

            # fix img lazy load


            data['content'] = fixLazyImg(str(article_body))
            data['image_url'] = ''
            data['author_id'] = 'meng-qing-xue-81'
            data['author_name'] = self.parse_creator_name()
            data['author_headline'] = ''
            data['author_avatar_url'] = 'https://pic4.zhimg.com/v2-38a89e42b40baa7d26d99cab9a451623_xl.jpg'
            data['author_gender'] = '0'
        except Exception as e:
            print e.message
            return []

        return data
