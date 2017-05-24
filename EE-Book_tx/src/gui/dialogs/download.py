#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import time

from src.container.books import Book
from src.gui.library import insert_library
from src.tools.config import Config
from PyQt4.Qt import QDialog, pyqtSignal, QProgressDialog
from PyQt4 import QtCore, QtGui

from PyQt4.QtCore import Qt, QThread, QTextCodec, QSettings, QVariant, QSize, QPoint
from src.gui.dialogs.ui_download import Ui_Dialog
from src.web.feeds.recipes.model import RecipeModel

from src.tools.path import Path
from src.login import Login
from src.main import EEBook
from src.constants import EPUBSTOR_DIR, LIBRARY_DIR, ISOTIMEFORMAT


QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))


class DownloadDialog(QDialog, Ui_Dialog):
    download = pyqtSignal(object)

    def __init__(self, recipe_model, book_view, parent=None):
        QDialog.__init__(self, parent)
        self.now_url = ''
        self.book_view = book_view

        self.setAttribute(Qt.WA_DeleteOnClose)      # 每次关闭对话框删除对话框所占的内存
        self.setupUi(self)
        self.recipe_model = recipe_model
        self.recipe_model.showing_count = 3     # TODO, 改掉这里的硬编码
        self.count_label.setText(
            # NOTE: Number of news sources
            ('%s news sources') % self.recipe_model.showing_count)

        self.download_button.setVisible(False)

        self.initialize_detail_box()
        self.detail_box.setVisible(False)

        self.recipes.setFocus(Qt.OtherFocusReason)
        self.recipes.setModel(self.recipe_model)
        self.recipes.setAlternatingRowColors(True)
        self.recipes.setHeaderHidden(False)

        self.show_password.stateChanged[int].connect(self.set_pw_echo_mode)
        self.download_button.clicked.connect(self.download_button_clicked)
        self.login_button.clicked.connect(self.login_button_clicked)

        self.setWindowTitle("Download")


        QtCore.QObject.connect(self.recipes, QtCore.SIGNAL("clicked (QModelIndex)"), self.row_clicked)

    def set_pw_echo_mode(self, state):
        self.password.setEchoMode(self.password.Normal if state == Qt.Checked else self.password.Password)

    def row_clicked(self, index):
        u"""
        哪一行被选中了
        :return:
        """
        url = str(self.recipes.model().data(index, QtCore.Qt.UserRole))
        self.now_url = url

        self.detail_box.setVisible(True)
        if url == 'zhihu':          # TODO: 改掉硬编码, 这里的信息(是否需要登录)应该用xml或数据库记录
            self.detail_box.setVisible(True)
            self.account.setVisible(True)
            self.blurb.setText('''
            <p>
            <b>%(title)s</b><br>
            %(cb)s<br/>
            %(description)s
            </p>
            ''' % dict(title='zhihu', cb='Created by: Frank',
                     description=u'https://github.com/knarfeh/EE-Book <br/>第一次使用,请登录!\
                      若不登录,将尝试用程序内置账号登陆,私人收藏夹将无法爬取'))
            self.zhihu = EEBook(recipe_kind='zhihu')    # 目前只有知乎需要登陆 需要将Path初始化
            self.login = Login(recipe_kind='zhihu', from_ui=True)
        elif url == 'jianshu':
            self.detail_box.setVisible(True)
            self.account.setVisible(False)
            self.blurb.setText('''
            <p>
            <b>%(title)s</b><br>
            %(cb)s <br/>
            %(description)s
            </p>
            ''' % dict(title='jianshu', cb='Created by: Frank',
                     description=u'https://github.com/knarfeh/jianshu2e-book'))
        elif url == 'sinablog':
            self.detail_box.setVisible(True)
            self.account.setVisible(False)
            self.blurb.setText('''
            <p>
            <b>%(title)s</b><br>
            %(cb)s <br/>
            %(description)s
            </p>
            ''' % dict(title='sinablog', cb='Created by: Frank',
                     description=u'https://github.com/knarfeh/SinaBlog2e-book'))
        else:
            self.detail_box.setVisible(False)
        return self.recipes.model().data(index, QtCore.Qt.UserRole)

    def initialize_detail_box(self,):
        # self.previous_urn = urn
        self.detail_box.setVisible(True)
        self.download_button.setVisible(True)
        self.detail_box.setCurrentIndex(0)

    def login_button_clicked(self):
        account = str(self.username.text())
        password = str(self.password.text())
        captcha = str(self.captcha.text())

        if not self.login.login(account=account, password=password, captcha=captcha):
            click_ok = QtGui.QMessageBox.information(self, u"登陆失败", u"啊哦，登录失败，可能需要输入验证码\n请尝试输入验证码")
            if click_ok:
                self.login.get_captcha(from_ui=True)
                return
        Config.remember_account_set = True
        Config._save()
        QtGui.QMessageBox.information(self, u"登陆成功", u"恭喜, 登陆成功, 登陆信息已经保存")
        self.username.setText('')
        self.password.setText('')
        self.captcha.setText('')

    def download_button_clicked(self):
        tags = str(self.custom_tags.text())

        # url_id = self.recipes.model.data(1, QtCore.Qt.UserRole)    # TODO: 获得选中的recipes
        url_id = str(self.row_clicked(self.recipes.currentIndex()))

        if url_id == 'None':
            QtGui.QMessageBox.information(self, u"Error", u"选择需要爬取的网站!")
            return

        readlist_content = self.plainTextEdit.toPlainText()

        if readlist_content == '':
            QtGui.QMessageBox.information(self, u"Error", u"请在文本框中输入网址")
            return

        read_list_path = Path.read_list_path

        readList_file = open(read_list_path, 'w')
        readList_file.write(readlist_content)

        readList_file.close()

        game = EEBook(recipe_kind=url_id)

        progress_dlg = QProgressDialog(self)        # TODO: 设置大小, 区域
        progress_dlg.setWindowModality(Qt.WindowModal)
        progress_dlg.setMinimumDuration(5)
        progress_dlg.setWindowTitle(u"请等待")
        progress_dlg.setLabelText(u"制作中...请稍候")
        progress_dlg.setCancelButtonText(u"取消")
        progress_dlg.resize(350, 250)
        progress_dlg.show()
        progress_dlg.setRange(0, 20)

        for i in range(0, 15):
            progress_dlg.setValue(i)
            QThread.msleep(100)

        for i in range(15, 20):
            progress_dlg.setValue(i)
            QThread.msleep(100)
            if progress_dlg.wasCanceled():
                QtGui.QMessageBox.information(self, u"Error", u"电子书制作失败, 请重新操作")
                return

            try:
                filename = game.begin()      # TODO: 一次只能生成一本书
            except TypeError:
                QtGui.QMessageBox.information(self, u"Error", u"第一次使用请登录")
                progress_dlg.close()
                return
            progress_dlg.close()

            info_filename = ','.join(filename)
            QtGui.QMessageBox.information(self, u"info", u"电子书"+str(info_filename)+u"制作成功")

            for item in filename:
                file_path = EPUBSTOR_DIR + '/' + item
                Path.copy(str(file_path+'.epub'), LIBRARY_DIR)
                file_name = os.path.basename(str(file_path))
                book_id = file_name.split('.epub')[0]

                Path.mkdir(LIBRARY_DIR + book_id)
                shutil.move(LIBRARY_DIR+book_id+'.epub', LIBRARY_DIR+book_id)

                book = Book(str(book_id))
                book.date = time.strftime(ISOTIMEFORMAT, time.localtime())
                book.tags += tags.replace(' ', '')
                book.tags += ','+str(self.now_url)
                if self.add_title_tag.isChecked():
                    book.tags += ','+str(book.title)
                insert_library(book)
            return

