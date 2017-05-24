#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import os
import sys
import zipfile

from lxml import etree

from bs4 import BeautifulStoneSoup

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

from ..constants import LIBRARY_DIR    # it's ok

RECOVER_PARSER = etree.XMLParser(recover=True, no_network=True)
NAMESPACES = {
    'dc': 'http://purl.org/dc/elements/1.1/',
}


class Book(object):
    u"""
    需要主动调用open方法才能获得相应的属性
    """
    _FILE = LIBRARY_DIR + '%s/%s.epub'

    def __init__(self, book_id=None):
        self.tags = 'EEBook'
        self.title = ''
        self.author = ''
        self.date = ''
        self.size = ''
        self.rating = ''
        self.publisher = ''
        self.published = ''
        if book_id:
            self.open(book_id)

    def fromstring(self, raw, parser=RECOVER_PARSER):
        return etree.fromstring(raw, parser=parser)

    def read_doc_props(self, raw):
        u"""

        :param raw: raw string of xml
        :return:
        """
        root = self.fromstring(raw)
        self.title = root.xpath('//dc:title', namespaces={'dc': NAMESPACES['dc']})[0].text
        self.author = root.xpath('//dc:creator', namespaces={'dc': NAMESPACES['dc']})[0].text

    def open(self, book_id=None):
        if book_id:
            self.book_id = book_id
        if not self.book_id:
            raise Exception('Book id not set')

        self.size = os.path.getsize(self._FILE % (self.book_id, self.book_id))
        sz_mult = 1.0/(1024**2)
        result = u'%.1f' % (self.size * sz_mult)
        self.size = u'<0.1' if result == u'0.0' else result

        self.f = zipfile.ZipFile(self._FILE % (self.book_id, self.book_id), 'r')
        soup = BeautifulStoneSoup(self.f.read('META-INF/container.xml'))

        oebps = soup.findAll('rootfile')[0]['full-path']
        folder = oebps.rfind(os.sep)
        self.oebps_folder = '' if folder == -1 else oebps[:folder+1]   # 找到oebps的文件夹名称

        oebps_content = self.f.read(oebps)
        self.read_doc_props(oebps_content)

        opf_bs = BeautifulStoneSoup(oebps_content)
        ncx = opf_bs.findAll('item', {'id': 'ncx'})[0]
        ncx = self.oebps_folder + ncx['href']     # 找到ncx的完整路径

        ncx_bs = BeautifulStoneSoup(self.f.read(ncx))

        self.chapters = [(nav.navlabel.text, nav.content['src']) for
                         nav in ncx_bs.findAll('navmap')[0].findAll('navpoint')]
        self.cover_href = self.chapters[0][1]    # 封面路径

        # cover_content = self.f.read('OEBPS/'+self.cover_href)
        # print u"cover_content:" + str(cover_content)    # TODO:html转jpg,作为封面,又是一个坑

    def get_chapter(self, num):
        return self.f.read(self.oebps_folder+self.chapters[num][1])

if __name__ == '__main__':
    book = Book('ink')
    print book.oebps_folder

    print book.title
    print book.author

    print u"封面的路径是:" + str(book.cover_href)
    print str(book.chapters).decode("unicode-escape").encode("utf-8")





