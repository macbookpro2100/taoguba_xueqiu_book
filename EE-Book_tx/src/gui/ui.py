#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import os
import shutil
import subprocess

from PyQt4 import QtGui
from PyQt4.QtGui import (QMainWindow, QDockWidget, QFileDialog, QTableWidgetItem,
                         QAction, QKeySequence, QTableWidget, QMessageBox, QMenu, QCursor,
                         QSplitter, QScrollArea, QHBoxLayout)
from PyQt4.QtCore import Qt, SIGNAL, QSettings, QVariant, QSize, QPoint, QTimer, QFile, QTextCodec

from src.tools.debug import Debug
from src.gui.dialogs.download import DownloadDialog
from src.web.feeds.recipes.model import RecipeModel
from src.gui.library import LibraryTableWidget, insert_library, get_library, remove_from_library
from src.gui.bookview import BookView
from src.gui.dialogs.helpform import HelpForm
from src.gui.book_details import BookDetails

from src.container.books import Book
from src.constants import *
from src.tools.path import Path
from src.resources import qrc_resources

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        # super(MainWindow, self).__init__(parent)
        QtGui.QMainWindow.__init__(self, parent)

        self.filename = ""
        self.read_method_build_in = False    # 若为False, 用系统自带的EPub阅读器打开
        self.library = get_library()

        self.book_view = BookView()
        # ###########actions############################
        self.addBookAction = self.create_action(
            u"添加EPub格式的电子书", self.add_book, QKeySequence.Open,
            QtGui.QIcon(":/open.png"), u"从文件系统中添加"
        )
        # TODO: 切图标
        self.removeAction = self.create_action(
            u"移除Epub格式的电子书", self.remove_book, None,
            QtGui.QIcon(":/remove.png"), u"移除EPub格式电子书"
        )
        # TODO: 切图标
        self.downloadAction = self.create_action(
            u"制作EPub格式电子书", self.make_book, None,
            QtGui.QIcon(":/download.png"), u"制作EPub格式电子书"
        )
        # TODO: 阅读电子书的图标
        self.readAction = self.create_action(
            u"阅读电子书", self.view_book, None,          # TODO
            QtGui.QIcon(":/read.png"), u"阅读电子书"
        )
        self.toolbarAction = self.create_action(
            u"切换工具栏", self.toggle_toolbar, None, None, None,
        )
        self.statusbarAction = self.create_action(
            u"切换状态栏", self.toggle_statusbar, None, None, None
        )
        self.bookDetailAction = self.create_action(
            u"打开书籍详情窗口", self.create_book_info_dock, None, None, None
        )
        self.aboutHelpAction = self.create_action(
            u"帮助", self.about_help, None, None, None,
        )
        self.setViewerAction = self.create_action(
            u"设置EPub阅读器", self.set_viewer, None,
            None, u"设置默认的电子书阅读器"
        )
        self.open_with_build_in_action = self.create_action(
            u"用软件自带EPub阅读器打开", self.view_book_with_build_in, None,
            None, None
        )

        self.open_with_os_action = self.create_action(
            u"用系统默认EPub阅读器打开", self.view_book_with_os, None,
            None, None
        )

        # ContextMenu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        self.contextMenu = QMenu(self)
        self.add_actions(self.contextMenu, (self.open_with_build_in_action, self.open_with_os_action))


        # ###########toolbar############################
        self.toolbar = self.addToolBar("&Options")
        self.toolbar.setObjectName('Options')
        self.add_actions(self.toolbar, (self.addBookAction, self.removeAction,
                         self.readAction, self.downloadAction))
        self.addToolBarBreak()
        self.toolbar.setVisible(True)
        # ###########menubar############################
        self.menu_bar = self.menuBar()
        self.editBook = self.menu_bar.addMenu("&Books")
        self.add_actions(self.editBook, (self.addBookAction, self.removeAction, self.downloadAction))

        self.viewMenu = self.menu_bar.addMenu("&View")
        self.add_actions(self.viewMenu, (self.toolbarAction, self.statusbarAction, self.bookDetailAction))

        self.settingMenu = self.menu_bar.addMenu("&Setting")
        self.add_actions(self.settingMenu, (self.setViewerAction, ))

        self.helpMenu = self.menu_bar.addMenu("&Help")
        self.add_actions(self.helpMenu, (self.aboutHelpAction, ))

        # Initialize a statusbar for the window
        status = self.statusBar()
        status.setSizeGripEnabled(False)

        self.setGeometry(100, 100, 1030, 800)

        self.centralWidget = QtGui.QWidget(self)

        self.search_label = QtGui.QLabel(self.centralWidget)
        self.search_label.setText(u'搜索:')
        self.searchLineEdit = QtGui.QLineEdit(self.centralWidget)
        self.library_table = LibraryTableWidget(self.book_view)
        self.library_table.setVisible(True)

        self.gridLayout = QtGui.QGridLayout(self.centralWidget)
        self.gridLayout.addWidget(self.search_label, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.searchLineEdit, 0, 1, 1, 15)
        self.gridLayout.addWidget(self.library_table, 1, 0, 1, 16)
        # self.scrollArea = QScrollArea()

        self.setCentralWidget(self.centralWidget)

        self.create_book_info_dock()
        settings = QSettings()
        size = settings.value("MainWindow/Size", QVariant(QSize(1030, 800))).toSize()
        self.resize(size)

        position = settings.value("MainWindow/Position", QVariant(QPoint(120, 100))).toPoint()
        self.move(position)
        self.restoreState(settings.value("MainWindow/State").toByteArray())

        self.setWindowTitle("EE-Book")
        QTimer.singleShot(0, self.loadInitialFile)
        self.update_library()
        self.create_connections()

    def create_book_info_dock(self):
        if getattr(self, 'dock', None):
            self.dock.show()
            return

        self.dock = QDockWidget("book details", self)
        self.dock.setObjectName('book details')
        self.dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.book_detail = BookDetails(self.book_view)
        self.dock.setWidget(self.book_detail)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)


    def showContextMenu(self, pos):
        u"""
        右键点击时调用的函数
        """
        # 菜单显示前，将它移动到鼠标点击的位置
        self.contextMenu.exec_(QCursor.pos())      # 在鼠标位置显示

    def update_library(self):
        self.library = get_library()

        self.library_table.clear()
        self.library_table.setStyleSheet("selection-background-color: blue")  # 设置选中背景色
        self.library_table.setRowCount(len(self.library['books']))
        self.library_table.setColumnCount(5)    # TODO: 改掉硬编码??
        self.library_table.setHorizontalHeaderLabels(['Title', 'Authors', 'Tags', 'Date', 'Size(MB)'])

        self.library_table.setAlternatingRowColors(True)
        self.library_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.library_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.library_table.setSelectionMode(QTableWidget.SingleSelection)

        self.model = QtGui.QStandardItemModel(self)
        for i, book in enumerate(self.library['books']):
            for j, cell in enumerate((book['title'], book['author'], book['tags'],
                                      book['date'], book['size'])):
                item = QTableWidgetItem(cell)
                item.setTextAlignment(Qt.AlignCenter)
                self.library_table.setItem(i, j, item)

        self.library_table.resizeColumnsToContents()

    def create_action(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered()"):
        u"""

        :param text:
        :param slot:
        :param shortcut:
        :param icon:
        :param tip:
        :param checkable:
        :param signal:
        :return:
        """
        action = QAction(text, self)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if shortcut is not None:
            action.setShortcut(shortcut)
        if icon is not None:
            action.setIcon(icon)
        if tip is not None:
            action.setToolTip(tip)
        if checkable is not None:
            action.setCheckable(checkable)
        return action

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def closeEvent(self, event):
        settings = QSettings()
        settings.setValue("MainWindow/Size", QVariant(self.size()))
        settings.setValue("MainWindow/Position", QVariant(self.pos()))
        settings.setValue("MainWindow/State", QVariant(self.saveState()))

    def loadInitialFile(self):
        settings = QSettings()
        fname = settings.value("LastFile").toString()
        if fname and QFile.exists(fname):
            ok, msg = self.movies.load(fname)
            self.statusBar().showMessage(msg, 5000)

    def toggle_toolbar(self):
        state = self.toolbar.isVisible()
        self.toolbar.setVisible(not state)

    def toggle_statusbar(self):
        state = self.statusbar.isVisible()
        self.statusbar.setVisible(not state)

    def add_book(self):
        u"""
        打开已经在文件系统的电子书到电子书管理器中
        :return:
        """
        # Get filename and show only .epub files    Mac 系统下返回的是native fiel dialog
        book_path = QtGui.QFileDialog.getOpenFileName(self, u'打开Epub格式电子书', ".", "(*.epub)")

        if str(book_path) is '':
            # 没有选中电子书
            return

        if os.path.dirname(str(book_path))+os.sep != str(LIBRARY_DIR):
            shutil.copy(str(book_path), LIBRARY_DIR)

        file_name = os.path.basename(str(book_path))
        book_id = file_name.split('.epub')[0]
        bookdata_book_catalog = LIBRARY_DIR+book_id

        Path.mkdir(bookdata_book_catalog)

        Debug.logger.debug(u"移入bookdata中的是:" + str(LIBRARY_DIR+file_name))
        Debug.logger.debug(u"bookdata中的书:" + str(bookdata_book_catalog))
        Debug.logger.debug(u"book_path:" + os.path.dirname(str(book_path)))
        if os.path.dirname(str(book_path)) != bookdata_book_catalog:
            try:
                shutil.move(LIBRARY_DIR+file_name, bookdata_book_catalog)
            except shutil.Error:
                Debug.logger.debug(u"TODO:添加过这个书,删除原来的书")
                pass
        else:
            Debug.logger.debug(u"是相同文件夹, 添加的是bookdata中的书")
        os.remove(LIBRARY_DIR+file_name)
        book = Book(book_id)
        book.date = time.strftime(ISOTIMEFORMAT, time.localtime())
        insert_library(book)
        self.update_library()

    def remove_book(self):
        u"""
        移除电子书
        :return:
        """
        book_id = self.library['books'][self.library_table.currentRow()]['book_id']
        remove_from_library(book_id)
        self.update_library()

    def make_book(self):
        u"""
        制作电子书
        :return:
        """
        download = QtGui.QDialog()
        ui = DownloadDialog(RecipeModel(), self.book_view)   # TODO: 将任务交给jobs模块,

        ui.exec_()
        self.update_library()
        del download

    def create_connections(self):
        self.library_table.itemDoubleClicked.connect(self.view_book)
        self.library_table.itemClicked.connect(self.row_clicked)
        self.searchLineEdit.textChanged.connect(self.search_text_changed)

    def row_clicked(self):
        current_row = self.library_table.currentRow()
        current_book = self.library['books'][current_row]
        self.book_detail.show_data(current_book)
        pass

    def view_book(self):
        u"""
        用电子书阅读器打开选中的电子书
        :return:
        """
        if not self.library_table.isItemSelected(self.library_table.currentItem()):
            QMessageBox.information(self, u"Error", u"请选定要打开的电子书")
            return

        # 判断是否用软件内置的EPub阅读器打开
        if self.read_method_build_in:
            self.view_book_with_build_in()
        else:
            self.view_book_with_os()

    def view_book_with_build_in(self):
        book_id = self.library['books'][self.library_table.currentRow()]['book_id']
        self.book_view.load_book(book_id)
        self.book_view.show()

    def view_book_with_os(self):
        book_id = self.library['books'][self.library_table.currentRow()]['book_id']
        epub_path = LIBRARY_DIR + '%s/%s.epub' % (book_id, book_id)
        if isosx:
            subprocess.call(["open", epub_path])
        elif iswindows:
            os.startfile(file)    # TODO: 需要测试
        elif islinux:
            subprocess.call(["xdg-open", file])    # TODO: 需要测试

    def set_viewer(self):
        u"""
        设置默认的EPub阅读器
        :return:
        """
        if self.read_method_build_in:
            read_method_info = u"系统默认的EPub格式阅读器"
        else:
            read_method_info = u"软件内置的EPub格式阅读器"
        question_info = u"""
        现在设定的EPub阅读器是 %s, 目前软件自带的EPub阅读器正在开发中, 还比较简陋, 但可以用来预览(如果系统没有装EPub格式阅读器), 点击确定进行切换, 点击取消不切换
        """ % read_method_info
        clicked = QMessageBox.question(self, "设置EPub阅读器", question_info,
                                       QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
        if clicked:
            self.read_method_build_in = not self.read_method_build_in

    def about_help(self):
        form = HelpForm("index.html")
        form.setWindowTitle('EE-Book Help')
        form.show()
        form.exec_()

    def search_text_changed(self, text):
        for i in range(self.library_table.rowCount()):
            match = False
            for j in range(self.library_table.columnCount()):
                item = self.library_table.item(i, j)
                if item.text().contains(text):
                    match = True
                    break
            self.library_table.setRowHidden(i, not match)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


