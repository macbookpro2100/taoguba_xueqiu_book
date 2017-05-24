# -*- coding: utf-8 -*-
import hashlib
import os
import os.path
import re
import urllib

from src.tools.config import Config
from src.tools.debug import Debug
from src.tools.http import Http
from src.tools.match import Match
from ..tools.controler import Control
from ..tools.extra_tools import ExtraTools


def cbk(blocknum, blocksize, totalsize):
    per = 100.0 * blocknum * blocksize / totalsize
    if per > 100:
        per = 100
    print '%.2f%%' % per


class ImageContainer(object):
    u"""
    根据href, 完成关于图片的各种操作, 包括md5, 下载图片等
    """

    def __init__(self, save_path=''):
        self.save_path = save_path
        self.container = {}
        self.md5 = hashlib.md5()
        return

    def set_save_path(self, save_path):
        self.save_path = save_path
        return

    def add(self, href):
        self.container[href] = self.create_image(href)
        return self.get_filename(href)

    def delete(self, href):
        del self.container[href]
        return

    def get_filename(self, href):
        image = self.container.get(href)
        if image:
            return image['filename']
        return ''

    def get_filename_list(self):
        return self.container.values()

    def download(self, index):
        image = self.container[index]
        filename = image['filename']
        href = image['href']
        # filename=href.split('/')[-1]

        if os.path.isfile(self.save_path + '/' + filename):
            return
        print 'Downloading picture:' + href + '   filename   ' + filename

        # urllib.urlretrieve(href, self.save_path + '/' + filename, cbk)



        if len(str(href)) < 300 and Match.isUrlOk(href):
            # Debug.print_in_single_line(u'Downloading picture: {}'.format(href))
            rely_url = str(href).split('@')[0]
            content = Http.get_content(url=rely_url, timeout=Config.timeout_download_picture)
        else:
            Debug.print_in_single_line(u"Href of the Picture seems wrong...")
            content = None
        if not content:
            return
        with open(self.save_path + '/' + filename, 'wb') as image:
            image.write(content)
        return

    def start_download(self):
        argv = {
            'function': self.download,  # 所有待存入数据库中的数据都应当是list
            'iterable': self.container,
        }
        Control.control_center(argv, self.container)
        return

    def create_image(self, href):
        u"""

        :param href:
        :return: {'filename': md5编码的文件名, 'href': href}
        """
        image = {'filename': self.create_filename(href), 'href': href}
        return image

    def create_filename(self, href):
        u"""
        根据 href 创建md5编码之后的文件名
        :param href:
        :return:
        """
        # filename=href.split('/')[-1]
        filename = ExtraTools.md5(href) + '.jpg'
        return filename
