#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
from PyQt4 import Qt
from PyQt4.Qt import (Qt, QLayout, QWidget, pyqtSignal, QWebView, QSize, QPropertyAnimation,
                      QEasingCurve, QSizePolicy, QPixmap, QRect, pyqtProperty, QDesktopServices,
                      QUrl, QPalette, QFontInfo, QApplication)
# from PyQt4.QtCore import QUrl

from math import floor
from src.tools.debug import Debug
from src.resources import qrc_resources
from src.ebooks.metadata.book.render import book_detail_to_html


def render_data(current_book, use_roman_numbers=True, all_fields=False):
    # TODO 修改为一部分display, 一部分不需要display, 由all_fields和display控制
    field_list = current_book
    # field_list = [(x, display) for x, display in field_list]
    return book_detail_to_html(current_book, field_list, 'TODO:default_author_link', True)


def render_html(current_book, css, vertical, widget, all_fields=False, render_data_func=None):
    u"""

    :param current_book:
    :param css:
    :param vertical:
    :param widget:
    :param all_fields:
    :param render_data_func:
    :return:
    """
    table, comment_fields = render_data(current_book, all_fields=all_fields, use_roman_numbers=True)

    def color_to_string(col):
        ans = '#000000'
        if col.isValid():
            col = col.toRgb()
            if col.isValid():
                ans = unicode(col.name())
        return ans

    font_info = QFontInfo(QApplication.font(widget))
    font_px = font_info.pixelSize() + 1
    font_family = unicode(font_info.family()).strip().replace('"', '')

    if not font_family:
        font_family = 'sans-serif'

    body_td_color = color_to_string(QApplication.palette().color(QPalette.Normal, QPalette.WindowText))

    template = u"""
    <html>
        <head>
        <style type="text/css">
            body, td {
                background-color: transparent;
                font-size: %dpx;
                font-family: "%s", sans-serif;
                color: %s
            }
        </style>
        <style type="text/css">
            %s
        </style>
        </head>
        <body>
        %%s
        </body>
    </html>
    """ % (font_px, font_family, body_td_color, css)
    comments = u''
    comment_fields = None
    if comment_fields:
        comments = '\n'.join(u'<div>%s</div>' % x for x in comment_fields)
    right_pane = u'<div id="comments" class="comments">%s</div>' % comments

    if vertical:
        ans = template % (table+right_pane)
    else:
        ans = template % (u'<table><tr><td valign="top" '
        'style="padding-right:2em; width:40%%">%s</td><td valign="top">%s</td></tr></table>'
                          % (table, right_pane))
    return ans


def open_url(qurl):
    if isinstance(qurl, basestring):
        qurl = QUrl(qurl)
    QDesktopServices.openUrl(qurl)


def fit_image(width, height, pwidth, pheight):
    u"""
    fit image in box of width pwidth and height pheight
    :param width: Width of image
    :param height: Height of image
    :param pwidth: Width of box
    :param pheight: Height of box
    :return: scaled, new_width, new_height, scaled is True if new_width and/or new_height is different
    from width or height.
    """
    scaled = height > pheight or width > pwidth
    if height > pheight:
        corrf = pheight / float(height)
        width, height = floor(corrf*width), pheight
    if width > pwidth:
        corrf = pwidth / float(width)
        width, height = pwidth, floor(corrf*height)
    if height > pheight:
        corrf = pheight / float(height)
        width, height = floor(corrf*width), pheight
    return scaled, int(width), int(height)


class CoverView(QWidget):
    u"""
    TODO: 实现点击图书显示封面的效果(再加一个coverflow的效果就完美了), 看来现在暂时搞不定了
    """
    cover_changed = pyqtSignal(object, object)
    cover_removed = pyqtSignal(object)
    open_cover_width = pyqtSignal(object, object)

    def __init__(self, vertical, parent=None):
        QWidget.__init__(self, parent)
        self._current_pixmap_size = QSize(120, 120)
        self.vertical = vertical

        self.animation = QPropertyAnimation(self, b'current_pixmap_size', self)
        self.animation.setEasingCurve(QEasingCurve(QEasingCurve.OutExpo))
        self.animation.setDuration(1000)
        self.animation.setStartValue(QSize(0, 0))
        # self.animation.valueChanged.connect(self.value_changed)

        self.setSizePolicy(
            QSizePolicy.Expanding if vertical else QSizePolicy.Minimum,
            QSizePolicy.Expanding
        )

        # self.default_pixmap = QPixmap(os.getcwd() + "/src/gui/code Examples/book.icns")
        self.default_pixmap = QPixmap(":/back.png")
        self.pixmap = self.default_pixmap
        self.pwidth = self.pheight = None
        self.data = {}

        self.do_layout()

    def value_changed(self, val):
        self.update()

    def setCurrentPixmapSize(self, val):
        self._current_pixmap_size = val

    def do_layout(self):
        if self.rect().width() == 0 or self.rect().height() == 0:
            return
        pixmap = self.pixmap
        pwidth, pheight = pixmap.width(), pixmap.height()
        try:
            self.pwidth, self.pheight = fit_image(pwidth, pheight,
                                                  self.rect().width, self.rect().height())[1:]
        except:
            self.pwidth, self.pheight = self.rect().width()-1, self.rect().height()-1
        self.current_pixmap_size = QSize(self.pwidth, self.pheight)
        self.animation.setEndValue(self.current_pixmap_size)

    def show_data(self, current_book):
        # self.animation.stop()
        # TODO
        if False:
            pass
        else:
            self.pixmap = self.default_pixmap
        # self.do_layout()
        # self.updatte()
        # self.animation.start()

    current_pixmap_size = pyqtProperty('QSize', fget=lambda self: self._current_pixmap_size,
                                       fset=setCurrentPixmapSize)

    def value_changed(self, val):
        # self.update()
        pass


class BookInfo(QWebView):
    link_clicked = pyqtSignal(object)
    # TODO
    remove_format = pyqtSignal(int, object)
    remove_item = pyqtSignal(int, object, object)
    save_format = pyqtSignal(int, object)
    restore_format = pyqtSignal(int, object)
    compare_format = pyqtSignal(int, object)
    # set_cover_format
    copy_link = pyqtSignal(object)
    manage_author = pyqtSignal(object)
    open_fmt_with = pyqtSignal(int, object, object)

    def __init__(self, vertical, parent=None):
        QWebView.__init__(self, parent)
        s = self.settings()
        s.setAttribute(s.JavascriptEnabled, False)
        self.vertical = vertical
        self.page().setLinkDelegationPolicy(self.page().DelegateAllLinks)
        self.linkClicked.connect(self.link_activated)
        self._link_clicked = False
        self.setAttribute(Qt.WA_OpaquePaintEvent, False)
        palette = self.palette()
        self.setAcceptDrops(False)
        palette.setBrush(QPalette.Base, Qt.transparent)
        self.page().setPalette(palette)
        # TODO
        self.css = ''
        self.setFocusPolicy(Qt.NoFocus)


    def link_activated(self, link):
        self._link_clicked = True
        if unicode(link.scheme()) in ('http', 'https'):
            return open_url(link)
        link = unicode(link.toString(QUrl.None))
        self.link_clicked.emit(link)

    def show_data(self, current_book):
        html = render_html(current_book, self.css, self.vertical, self.parent())
        self.setHtml(html)


class DetailsLayout(QLayout):
    def __init__(self, vertical, parent):
        QLayout.__init__(self, parent)
        self.vertical = vertical
        self._children = []
        self.min_size = QSize(190, 200) if vertical else QSize(120, 120)
        self.setContentsMargins(0, 0, 0, 0)

    def minimumSize(self):
        return QSize(self.min_size)

    def addItem(self, child):
        if len(self._children) > 2:
            raise ValueError('This layout can only manage two children')
        self._children.append(child)

    def itemAt(self, i):
        try:
            return self._children[i]
        except:
            pass
        return None

    def takeAt(self, i):
        try:
            self._children.pop(i)
        except:
            pass
        return None

    def count(self):
        return len(self._children)

    def sizeHint(self):
        return QSize(self.min_size)

    def setGeometry(self, r):
        QLayout.setGeometry(self, r)
        self.do_layout(r)

    def cover_height(self, r):
        if not self._children[0].widget().isVisible():
            return 0
        mw = 1 + int(3/4. * r.height())
        try:
            pw = self._children[0].widget().pixmap.width()
        except:
            pw = 0
        if pw > 0:
            mw = min(mw, pw)
        return mw

    def do_layout(self, rect):
        if len(self._children) != 2:
            return
        left, top, right, bottom = self.getContentsMargins()
        r = rect.adjusted(+left, +top, -right, -bottom)
        x = r.x()
        y = r.y()
        cover, details = self._children

        if self.vertical:
            ch = self.cover_height(r)
            cover.setGeometry(QRect(x, y, r.width(), ch))
            cover.widget().do_layout()
            y += ch + 5
            details.setGeometry(QRect(x, y, r.width(), r.height()-ch-5))
        else:
            cw = self.cover_width(r)
            cover.setGeometry(QRect(x, y, cw, r.height()))
            cover.widget().do_layout()
            x += cw + 5
            details.setGeometry(QRect(x, y, r.width()-cw-5, r.height()))


class BookDetails(QWidget):
    show_book_info = pyqtSignal()

    def __init__(self, vertical, parent=None):
        QWidget.__init__(self, parent)
        self._layout = DetailsLayout(vertical, self)
        self.setLayout(self._layout)
        self.current_path = ''

        self.cover_view = CoverView(vertical, self)

        self._layout.addWidget(self.cover_view)

        self.book_info = BookInfo(vertical, self)
        self._layout.addWidget(self.book_info)

        self.book_info.link_clicked.connect(self.handle_click)
        self.setCursor(Qt.PointingHandCursor)

    def handle_click(self, link):
        pass

    def mouseDoubleClickEvent(self, QMouseEvent):
        QMouseEvent.accept()
        pass

    def show_data(self, current_book):
        self.book_info.show_data(current_book)
        self.cover_view.show_data(current_book)
        # self.current_path = getattr(data, u'path', u'')
        # self.updata_layout()

    def updata_layout(self):
        self.cover_view.setVisible(True)
        self._layout.do_layout(self.rect())
        # TODO


    def reset_info(self):
        # TODO
        pass


