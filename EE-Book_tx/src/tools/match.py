# -*- coding: utf-8 -*-
import re

from src.tools.debug import Debug
from src.tools.type import ImgQuality


class Match(object):
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
        return re.search(r'(?<=zhihu\.com/)people/(?P<author_page_id>[^/\n\r]*)', content)

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
    def wechat(content=''):
        return re.search(r'(?<=chuansong\.me/account/)(?P<account_id>[^/?\n\r]*)', content)

    @staticmethod
    def wuxia(content=''):
        u"""
https://www.wuxiareview.com/category/
        :return:
        """
        return re.search(r'(?<=wuxiareview\.com/category/)(?P<account_id>[^/\n\r]*)', content)
    @staticmethod
    def jinwankansa(content=''):
        u"""
http://www.jintiankansha.me/column/2u6annmY7Q
        :return:
        """
        return re.search(r'(?<=jintiankansha\.me/column/)(?P<account_id>[^/\n\r]*)', content)

    @staticmethod
    def doc360(content=''):
        u"""
http://www.360doc.com/userhome/40033985
        :return:
        """
        return re.search(r'(?<=360doc\.com/userhome/)(?P<account_id>[^/\n\r]*)', content)

    @staticmethod
    def huawei(content=''):
        u"""
http://xinsheng.huawei.com/cn/index.php?app=forum&mod=List&act=index&class=461&cate=155&search=%E4%BB%BB%E6%80%BB&p=1

        :return:
        """
        return re.search(r'(?<=huawei\.com/)(?P<haccount_id>[^/\n\r]*)', content)

    @staticmethod
    def wechat_article_index(content=''):
        """
        直接在文件中匹配出微信文章地址
        :param content:
        :return:
        """
        return re.findall(r'(?<=href="/n/)\d+', content)

    @staticmethod
    def html_body(content=''):
        return re.search('(?<=<body>).*(?=</body>)', content, re.S).group(0)


    @staticmethod
    def sina(content=''):
        u"""
        TODO: 这样的链接也是可以的: http://blog.sina.com.cn/1340398703, 以及这样的:
        http://blog.sina.com.cn/caicui
        :param content: Sina博客网址, 如:http://blog.sina.com.cn/u/1287694611
        :return:  re.match object
        """
        return re.search(r'(?<=blog\.sina\.com\.cn/u/)(?P<sinablog_people_id>[^/\n\r]*)', content)

    @staticmethod
    def huxiu(content=''):
        u"""

        :param content: huxiu 博主主页地址, http://www.huxiu.com/buptzym/
        :return:
        """
        return re.search(r'(?<=huxiu\.com/)(?P<huxiu_id>[^/\n\r]*)', content)

    @staticmethod
    def xueqiu(content=''):
        u"""
        :param content: https://xueqiu.com/4065977305
        :return:
        """
        return re.search(r'(?<=xueqiu\.com/u/)(?P<xueqiu_author_id>[^/\n\r]*)', content)

    @staticmethod
    def todo(content=''):
        u"""
        :param content: https://xueqiu.com/4065977305
        :return:
        """
        return re.search(r'(?<=gushequ\.com/)(?P<account_id>[^/\n\r]*)', content)
    @staticmethod
    def todo1(content=''):
        u"""
        :param content:   guancha.cn
        :return:
        """
        return re.search(r'(?<=guancha\.cn/)(?P<account_id>[^/\n\r]*)', content)
    @staticmethod
    def todo2(content=''):
        u"""
        :param content: https://xueqiu.com/4065977305 cn.nytimes.com
        :return:
        """
        return re.search(r'(?<=cn\.nytimes\.com/)(?P<account_id>[^/\n\r]*)', content)
    @staticmethod
    def fiel(content=''):
        u"""
        :param content: https://xueqiu.com/4065977305 cn.nytimes.com
        :return:
        """
        return re.search(r'(?<=fiel\.com/)(?P<account_id>[^/\n\r]*)', content)
    @staticmethod
    def zhengshitang(content=''):
        u"""
        :param content: https://xueqiu.com/4065977305
        :return:
        """
        return re.search(r'(?<=zhengshitang\.com/)(?P<z_author_id>[^/\n\r]*)', content)

    @staticmethod
    def buffett(content=''):
        u"""
        :param content: https://xueqiu.com/4065977305
        :return:
        """
        return re.search(r'(?<=cnbc\.com/)(?P<todo_id>[^\n\r]*)', content)



    @staticmethod
    def taoguba_article(content=''):
        u"""
        :param content:
            http://blog.sina.com.cn/s/articlelist_1287694611_0_1.html
        :return:
        """
        return re.search(r'(?<=taoguba\.com\.cn/Article/)(?P<article_id>[^/\n\r]*)(/)(?P<range_id>[^/\n\r]*)', content)



    @staticmethod
    def fix_html(content=''):
        content = content.replace('</br>', '').replace('</img>', '')
        content = content.replace('<br>', '<br/>')
        content = content.replace('href="//link.zhihu.com', 'href="https://link.zhihu.com')  # 修复跳转链接
        for item in re.findall(r'\<noscript\>.*?\</noscript\>', content, re.S):
            content = content.replace(item, '')
        return content

    @staticmethod
    def fix_filename(filename):
        return Match.replace_danger_char_for_filesystem(filename)[:80]

    @staticmethod
    def replace_danger_char_for_filesystem(filename):
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
            '\r': '',
            '&': 'and',
        }
        for key, value in illegal.items():
            filename = filename.replace(key, value)
        return unicode(filename)

    @staticmethod
    def generate_img_src(img_file_name ='da8e974dc.jpg', img_quality=ImgQuality.big):
        """
        生成特殊的图片地址(知乎头像/专栏信息等存在于数据库中的图片)
        :param img_file_name: 图片名
        :param img_quality: 图片质量
        :return:
        """
        result = re.search(r'(?<=zhimg.com/)(?P<name>[^_]*)[^\.]*\.(?P<ext>.*)', img_file_name)
        if not result:
            # 地址不符合规范，直接返回false
            return None

        filename = result.group('name')
        ext = result.group('ext')

        if img_quality == ImgQuality.raw:
            img_file_name = filename + '.' + ext
        elif img_quality == ImgQuality.big:
            img_file_name = filename + '_b.' + ext
        elif img_quality == ImgQuality.none:
            return ''
        else:
            Debug.logger.info('警告：图片类型设置不正确！')
            return None
        url = ImgQuality.add_random_download_address_header_for_img_filename(img_file_name)
        return url

    def fix_image(self, content):
        content = Match.fix_html(content)
        for img in re.findall(r'<img[^>]*', content):
            # fix img
            if img[-1] == '/':
                img = img[:-1]
            img += '>'

            src = re.search(r'(?<=src=").*?(?=")', img)
            if not src:
                new_image = img + '</img>'
                content = content.replace(img, new_image)
                continue
            else:
                src = src.group(0)
                if src.replace(' ', '') == '':
                    new_image = img + '</img>'
                    content = content.replace(img, new_image)
                    continue
                else:
                    new_image = '<img>'

            new_image += '</img>'
            content = content.replace(img, '<div class="duokan-image-single">{}</div>'.format(new_image))

        return content

    @staticmethod
    def match_img_with_src_dict(content):
        img_src_dict = {}
        img_list = re.findall(r'<img[^>]*>', content)
        for img in img_list:
            result = re.search(r'(?<=src=").*?(?=")', img)

            if not result:
                img_src_dict[img] = ''
            else:
                src = result.group(0)
                if 'zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg' in src :
                    result = re.search(r'(?<=data-original=").*?(?=")', img)
                    img_src_dict[img] = result.group(0)
                if 'read.html5.qq.com/image' in src:
                    result = re.search(r'(?<=imageUrl=).*?(?=")', img)
                    img_src_dict[img] = result.group(0)
                else:
                    if str(src).__len__() < 1:
                        print img
                    img_src_dict[img] = src
        return img_src_dict

    @staticmethod
    def create_img_element_with_file_name(filename):
        src = Match.create_local_img_src(filename)
        return u'<div class="duokan-image-single"><img src="{}"></img></div>'.format(src)
    @staticmethod
    def avatar_create_img_element_with_file_name(filename):
        src = Match.create_local_img_src(filename)
        return u'<div class="duokan-image-single"><img src="{}" height="30" width="30"></img></div>'.format(src)
    @staticmethod
    def create_local_img_src(filename):
        u"""
        生成本地电子书图片地址
        :param filename:
        :return:
        """
        src = '{}'.format(u'../images/' + filename)
        return src




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
    def replace_specile_chars(text):
        r1 = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+'

        text = text.decode("utf8")
        return re.sub(r1.decode("utf8"), "".decode("utf8"), text)
    @staticmethod
    def replace_stimespecile_chars(text):
        r1 = u'[a-zA-Z’!"#$%&\'()*+,./;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+'

        text = text.decode("utf8")
        return re.sub(r1.decode("utf8"), "".decode("utf8"), text)