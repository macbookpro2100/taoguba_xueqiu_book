# -*- coding: utf-8 -*-
import re

from type import Type
from ..exception import UnsupportTypeException

r1 = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'


class Match(object):
    # zhihu
    @staticmethod
    def xsrf(content=''):
        xsrf = re.search(r'(?<=name="_xsrf" value=")[^"]*(?="/>)', content)
        if xsrf:
            return '_xsrf=' + xsrf.group(0)
        return ''

    @staticmethod
    def answer(content=''):
        return re.search(r'(?<=zhihu\.com/)question/(?P<question_id>\d{8})/answer/(?P<answer_id>\d{8})', content)

    @staticmethod
    def question(content=''):
        return re.search(r'(?<=zhihu\.com/)question/(?P<question_id>\d{8})', content)

    @staticmethod
    def author(content=''):
        return re.search(r'(?<=zhihu\.com/)people/(?P<author_id>[^/\n\r]*)', content)

    @staticmethod
    def collection(content=''):
        return re.search(r'(?<=zhihu\.com/)collection/(?P<collection_id>\d*)', content)

    @staticmethod
    def topic(content=''):
        return re.search(r'(?<=zhihu\.com/)topic/(?P<topic_id>\d*)', content)

    @staticmethod
    def article(content=''):
        return re.search(r'(?<=zhuanlan\.zhihu\.com/)(?P<column_id>[^/]*)/(?P<article_id>\d{8})', content)

    @staticmethod
    def column(content=''):
        return re.search(r'(?<=zhuanlan\.zhihu\.com/)(?P<column_id>[^/\n\r]*)', content)

    @staticmethod
    def html_body(content=''):
        return re.search('(?<=<body>).*(?=</body>)', content, re.S).group(0)

    # jianshu
    @staticmethod
    def jianshu_author(content=''):
        u"""

        :param content: jianshu个人主页的地址
        :return: re.match object
        """
        return re.search(r'(?<=jianshu\.com/users/)(?P<jianshu_id>[^/\n\r]*)(/latest_articles)', content)

    @staticmethod
    def jianshu_collection(content=''):
        u"""

        :param content: jianshu collection url
        :return: re.match object
        """
        return re.search(r'(?<=jianshu\.com/c/)(?P<collection_id>[^/\n\r]*)', content)

    @staticmethod
    def jianshu_notebooks(content=''):
        u"""

        :param content: jianshu notebooks url
        :return:
        """
        return re.search(r'(?<=jianshu\.com/notebooks/)(?P<notebooks_id>[^/\n\r]*)(/)', content)

    @staticmethod
    def jianshu_article_id(content=''):
        u"""

        :param content:
        :return:
        """
        return re.search(r'(?<=www\.jianshu\.com/p/)(?P<jianshu_article_id>[^/\n\r\']*)()', content)

    # sinablog
    @staticmethod
    def sinablog_author(content=''):
        u"""
        TODO: 这样的链接也是可以的: http://blog.sina.com.cn/1340398703, 以及这样的:
        http://blog.sina.com.cn/caicui
        :param content: Sina博客网址, 如:http://blog.sina.com.cn/u/1287694611
        :return:  re.match object
        """
        return re.search(r'(?<=blog\.sina\.com\.cn/u/)(?P<sinablog_people_id>[^/\n\r]*)', content)

    @staticmethod
    def sinablog_profile(content=''):
        u"""

        :param content: Sina博客"博客目录"的网址, 如:
            http://blog.sina.com.cn/s/articlelist_1287694611_0_1.html
        :return:
        """
        return re.search(r'(?<=blog\.sina\.com\.cn/s/articlelist_)(?P<sinablog_people_id>[^/\n\r]*)(_0_1\.)', content)

    # cnblogs
    @staticmethod
    def cnblogs_author(content=''):
        u"""

        :param content: cnblogs 博主主页地址, http://www.cnblogs.com/buptzym/
        :return:
        """
        return re.search(r'(?<=cnblogs\.com/)(?P<cnblogs_id>[^/\n\r]*)(/)', content)

    # csdn
    @staticmethod
    def csdnblog_author(content=''):
        u"""

        :param content: csdn 博主主页地址, http://blog.csdn.net/elton_xiao
        :return: re.match object
        """
        return re.search(r'(?<=blog\.csdn\.net/)(?P<csdnblog_author_id>[^/\n\r]*)', content)

    # generic
    @staticmethod
    def yiibai(content=''):
        u"""

        :param content: yiibai , http://www.yiibai.com,
        :return:
        """
        return re.search(r'(?<=yiibai\.com/)(?P<subject_id>[^/\n\r]*)(/)', content)

    @staticmethod
    def talkpython(content=''):
        u"""

        :param content: http://talkpython.fm
        :return:
        """
        return re.search(r'(?<=talkpython\.fm/episodes/)(?P<subject_id>[^/\n\r]*)(/)', content)

    # taoguba
    @staticmethod
    def taoguba_author(content=''):
        u"""
        :param content: http://www.taoguba.com.cn/Article/1483634/
        :return:
        """
        return re.search(r'(?<=taoguba\.com\.cn/Article/)(?P<article_id>[^/\n\r]*)(/)', content)

    @staticmethod
    def taoguba_article(content=''):
        u"""

        :param content:
            http://blog.sina.com.cn/s/articlelist_1287694611_0_1.html
        :return:
        """
        return re.search(r'(?<=taoguba\.com\.cn/Article/)(?P<article_id>[^/\n\r]*)(/)(?P<range_id>[^/\n\r]*)', content)

    @staticmethod
    def xueqiu_author(content=''):
        u"""
        :param content: https://xueqiu.com/4065977305
        :return:
        """
        return re.search(r'(?<=xueqiu\.com/)(?P<xueqiu_author_id>[^/\n\r]*)', content)

    @staticmethod
    def stripTags(s):
        intag = [False]

        def chk(c):
            if intag[0]:
                intag[0] = (c != '>')
                return False
            elif c == '<':
                intag[0] = True
                return False
            return True

        return ''.join(c for c in s if chk(c))


    @staticmethod
    def fix_filename(filename):
        illegal = {
            '\\': '＼',
            '/': '',
            ':': '：',
            '*': '＊',
            '?': '？',
            '<': '《',
            '>': '》',
            '|': '｜',
            '"': '〃',
            '!': '！',
            '\n': '',
            '\r': ''
        }
        for key, value in illegal.items():
            filename = filename.replace(key, value)
        return unicode(filename[:80])

    @staticmethod
    def fix_html(content='', recipe_kind=''):
        content = content.replace('</br>', '').replace('</img>', '')
        content = content.replace('<br>', '<br/>')
        content = content.replace('<wbr>', '').replace('</wbr>', '<br/>')  # for sinablog
        content = content.replace('href="//link.zhihu.com', 'href="https://link.zhihu.com')  # 修复跳转链接
        # 修复 taoguba 跳转链接

        content = content.replace('href="blog/', 'href="http://www.taoguba.com.cn/blog/')

        # for SinaBlog
        if recipe_kind in Type.sinablog:
            for item in re.findall(r'\<span class="img2"\>.*?\</span\>', content):
                content = content.replace(item, '')
            for item in re.findall(r'\<script\>.*?\</script\>', content, re.S):
                content = content.replace(item, '')
            for item in re.findall(r'height=\".*?\" ', content):  # 因为新浪博客的图片的高,宽是js控制的,不加
                content = content.replace(item, '')  # 这一段会导致无法匹配图片
            for item in re.findall(r'width=\".*?\" ', content):
                content = content.replace(item, '')
            for item in re.findall(r'\<cite\>.*?\</cite\>', content):
                content = content.replace(item, '')

        for item in re.findall(r'\<noscript\>.*?\</noscript\>', content, re.S):
            content = content.replace(item, '')
        return content

    @staticmethod
    def detect_recipe_kind(command):
        u"""

        :param command:
        :return: command_type, e.g. sinablog_author, answer, column
        """
        for command_type in Type.type_list:
            result = getattr(Match, command_type)(command)
            if result:
                return command_type
        return 'unknown'

    @staticmethod
    def get_url_kind(url):
        u"""
        for --info, Similar to get_recipe_kind, but accept more general type
        :param url:
        :return: website kind,
        """
        split_url = url.split('#')[0]  # remove comment of raw url
        split_url = split_url.split('$')[0]  # the first one determine type

        kind = 'Unknow type'
        for keyword in Type.key_word_to_website_type.keys():
            if split_url.find(keyword) >= 0:
                kind = Type.key_word_to_website_type[keyword]
        if kind == 'Unknow type':
            raise UnsupportTypeException('Getting website info..')
        return kind

    @staticmethod
    def isUrlOk(url):

        return re.match(r'^https?:/{2}\w.+$', url) or re.match(r'^http?:/{2}\w.+$', url)

    @staticmethod
    def get_website_kind(url):
        u"""

        :param url: one line
        :return: website kind, e.g. 'zhihu', 'jianshu', 'sinablog', 'csdnblog'

        """
        print url
        split_url = url.split('#')[0]  # remove comment of raw url
        split_url = split_url.split('$')[0]  # the first one determine type
        url_type = Match.detect_recipe_kind(split_url)

        website_kind = 'Unsupport type'
        for website in Type.website_type.keys():
            if url_type in getattr(Type, website):
                website_kind = website
        if website_kind == 'Unsupport type':
            raise UnsupportTypeException('Detecting website kind...')
        return website_kind

    @staticmethod
    def replace_words(text, word_dic):
        re_obj = re.compile('|'.join(map(re.escape, word_dic)))

        def translate(mat):
            return word_dic[mat.group(0)]

        return re_obj.sub(translate, text)

    @staticmethod
    def replace_specile_chars(text):
        r1 = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+'

        text = text.decode("utf8")
        return re.sub(r1.decode("utf8"), "".decode("utf8"), text)
