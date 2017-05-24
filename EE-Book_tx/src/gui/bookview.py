#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webbrowser

from PyQt4.QtGui import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
                         QListWidget, QLabel, QSplitter, QMessageBox,
                         QProgressDialog, QMainWindow)
from PyQt4.QtWebKit import QWebView, QWebPage
from PyQt4.QtCore import SIGNAL

from src.container.books import Book
from src.gui.library import insert_library


class BookView(QSplitter, QMainWindow):

    def __init__(self, parent=None):
        super(BookView, self).__init__(parent=parent)

        self.create_layout()
        self.create_connections()

    def create_layout(self):
        self.web_view = QWebView()

        self.chapter_list = QListWidget()

        self.next_button = QPushButton("Next chapter")
        self.previous_button = QPushButton("Previous chapter")

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.previous_button)
        hbox.addWidget(self.next_button)

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("Chapters"))
        vbox.addWidget(self.chapter_list)
        vbox.addLayout(hbox)

        widget = QWidget()
        widget.setLayout(vbox)

        self.addWidget(self.web_view)
        self.addWidget(widget)

    def create_connections(self):
        chlist = self.chapter_list
        self.connect(self.next_button, SIGNAL("clicked()"), lambda:
                     chlist.setCurrentRow(0
                         if chlist.currentRow() == chlist.count() - 1
                         else chlist.currentRow() + 1))
        self.connect(self.previous_button, SIGNAL("clicked()"), lambda:
                     chlist.setCurrentRow(chlist.count() - 1
                                          if chlist.currentRow() == 0
                                          else chlist.currentRow() - 1))
        self.connect(self.chapter_list, SIGNAL("currentRowChanged(int)"),
                     self.set_chapter)

        page = self.web_view.page()
        page.setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        # self.connect(page, SIGNAL("linkClicked(const QUrl&)"),
        #              self.link_clicked)

    def load_book(self, book_id):
        self.book = Book(book_id)
        self.chapter_list.clear()
        for chapter in self.book.chapters:
            self.chapter_list.addItem(chapter[0])
        self.chapter_list.setCurrentRow(0)

    def set_chapter(self, num=None):
        if num is None:
            num = self.chapter_list.currentRow()
        if num < 0:
            num = len(self.book.chapters) - 1
        elif num >= len(self.book.chapters):
            num = 0
        self.web_view.setHtml(self.book.get_chapter(num).decode(encoding="utf-8"))


