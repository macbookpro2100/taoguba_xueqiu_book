# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from src.lib.wechat_parser.tools.parser_tools import ParserTools
from src.tools.config import Config
from src.tools.match import Match
import re
import datetime
import time


from collections import OrderedDict


def date_format(time_string):
    """
    function: format item[date]
    by zhongp 2016-11-29
    Tips：
    Input time_string should be formated to string like "%Y-%m-%d" or "%Y-%m-%d %H:%M" or "%Y-%m-%d %H:%M:%S"
    or current time will be returned.
    """

    if time_string is None:
        return ''

    now = datetime.datetime.now()
    nowdatestr = now.strftime("%Y-%m-%d")
    nowdate = datetime.datetime.strptime(nowdatestr, "%Y-%m-%d")
    nowtimestr = now.strftime("%H:%M:%S")

    if re.match(r"\d\d\d\d-\d+-\d+ \d+:\d+:\d+", time_string):
        pass
    elif re.match(r"\d\d\d\d-\d+-\d+ \d+:\d+", time_string):
        time_string = time_string + ":00"
    elif re.match(r"\d\d\d\d-\d+-\d+", time_string):
        ts = datetime.datetime.strptime(time_string[0:10], "%Y-%m-%d")
        if nowdate > ts:
            time_string = ts.strftime("%Y-%m-%d") + " 23:59:00"
        else:
            time_string = ts.strftime("%Y-%m-%d") + " " + nowtimestr
    elif re.match(ur'\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}', time_string):
        # added by zhangz@2017-01-23 for match pattern like: 2017年01月03日 08:19
        ts = datetime.datetime.strptime(time_string.encode('utf8'), "%Y年%m月%d日 %H:%M")
        time_string = ts.strftime("%Y-%m-%d %H:%M:00")
    elif re.match(r'\d{2}-\d{2} \d{2}:\d{2}', time_string):
        # added by zhangz@2016-12-09 for match pattern like: 12-06 17:54
        time_string = "%04s" % now.year + "-" + time_string + ":00"
    # added by guow@2018-06-13 for
    elif time_string == '今天':
        time_string = nowdatestr + " " + nowtimestr
    elif time_string == '昨天':
        time_string = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d") + " 23:59:00"
    elif time_string == '前天':
        time_string = (now - datetime.timedelta(days=2)).strftime("%Y-%m-%d") + " 23:59:00"
    elif re.match(ur'\d天前', time_string):
        days_ago = int(re.findall(ur'\d+', time_string)[0])
        time_string = (now - datetime.timedelta(days=days_ago)).strftime("%Y-%m-%d") + " 23:59:00"
    elif re.match(ur'\d周前', time_string):
        week_ago = int(re.findall(ur'\d+', time_string)[0])
        time_string = (now - datetime.timedelta(days=week_ago*7)).strftime("%Y-%m-%d") + " 23:59:00"
    elif re.match(ur'\d+月\d+日', time_string):
        ts = datetime.datetime.strptime(time_string.encode('utf8'), "%m月%d日")
        time_string = '%s-%s 23:59:00' % (now.strftime('%Y'), ts.strftime("%m-%d"))
    else:
        time_string = nowdatestr + " " + nowtimestr

    return time_string

def news_date_format(time_string):
    """
        call date_format,
        and calc the right time of a news_date
        rely on zp's date_format.
        WHY? time_string have to be early than NOW
    """
    format_str = date_format(time_string)
    ## ensure it is a legal datetime
    now_datetime = datetime.datetime.now()
    format_datetime = datetime.datetime.strptime(format_str, "%Y-%m-%d %H:%M:%S")
    if format_datetime > now_datetime:
        format_str = datetime.datetime.strftime(format_datetime, "%04d" % (format_datetime.year-1) + "-%m-%d %H:%M:%S")
    return format_str


class WeiXinColumnParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'html.parser')

    def get_column_info(self):
        data = {}



        data['article_count'] = 0
        data['follower_count'] = 0
        data['description'] = ''
        data['image_url'] = ''

        return data


class WeiXinArticleParser(ParserTools):
    def __init__(self, content):
        self.dom = BeautifulSoup(content, 'lxml')

    def get_article_info(self):
        data = {}
        try:
            try:
                title_tationl = self.dom.find_all('h2')
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

            # content0 = self.dom.find_all('div', class_="rich_media_thumb_wrp")[0]
            content = self.dom.find_all('div', class_="rich_media_content")[0]
            article_body += str(content)
            data['content'] = str(article_body)

            time_tationl = self.dom.find_all('div', class_="rich_media_meta_list")[0]

            ddm =  BeautifulSoup(str(time_tationl), 'lxml')
            # print ddm
            lk = ddm.find_all('span', class_="rich_media_meta rich_media_meta_nickname")[0]
            try:
                lkk = lk.find_all('a', id="js_name")[0]
                data['author_name'] = str(lkk.text).strip()
            except Exception:
                data['author_name'] = ''
            # try:
            #
            #    extract_script = self.dom.find('script', text=re.compile('var publish_time'))
            #    extract_date = re.findall("\d+-\d+-\d+", re.findall(
            #            'var publish_time = "\d+-\d+-\d+"', extract_script.string)[0])[0]
            #    date_str = news_date_format(extract_date)
            #
            #
            #    pubtime = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            #
            #    print pubtime.strftime('%Y-%m-%d')
            #    data['updated_time'] = pubtime.strftime('%Y-%m-%d')
            #
            # except Exception:
            #     #TODO fix time

            tk = ddm.find_all('em', id="publish_time")[0]

            date_str = news_date_format(tk.text)


            pubtime = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

            print pubtime.strftime('%Y-%m-%d')
            data['updated_time'] = pubtime.strftime('%Y-%m-%d')


            # print data['updated_time']
            data['voteup_count'] =  ""
            data['comment_count'] = ""

            data['image_url'] = ''

            data['author_id'] = 'meng-qing-xue-81'



            data['author_headline'] = ''
            data['author_avatar_url'] = 'https://pic4.zhimg.com/v2-38a89e42b40baa7d26d99cab9a451623_xl.jpg'
            data['author_gender'] = '0'
        except Exception as e:
            print e.message
            return []

        return data