#!/usr/bin/env python

import re
import time


from PyQt4.Qt import (QAbstractTableModel, QModelIndex, Qt,
    QTimer, pyqtSignal, QIcon, QDialog, QAbstractItemDelegate, QApplication,
    QSize, QStyleOptionProgressBar, QStyle, QToolTip, QFrame,
    QHBoxLayout, QVBoxLayout, QSizePolicy, QLabel, QCoreApplication, QAction,
    QByteArray, QSortFilterProxyModel, QTextBrowser, QPlainTextEdit)

from src.gui.dialogs.job_ui import Ui_JobsDialog



class JobsDialog(QDialog, Ui_JobsDialog):
    def __init__(self):
        QDialog.__init__(self)
        Ui_JobsDialog.__init__(self)
        self.setupUi(self)
        # self.model = model
        # self.proxy_model = FilterModel(self)
        # self.proxy_model.setSourceModel(self.model)
        # self.proxy_model.search_done.connect(self.search.search_done)
        # self.jobs_view.setModel(self.proxy_model)
        self.setWindowModality(Qt.NonModal)
        self.setWindowTitle('EE-Book' + (' - Jobs'))     # TODO
        self.details_button.clicked.connect(self.show_details)
        self.kill_button.clicked.connect(self.kill_job)
        self.stop_all_jobs_button.clicked.connect(self.kill_all_jobs)
        # self.pb_delegate = ProgressBarDelegate(self)    # TODO
        # self.jobs_view.setItemDelegateForColumn(2, self.pb_delegate)
        # self.jobs_view.doubleClicked.connect(self.show_job_details)
        # self.jobs_view.horizontalHeader().setSectionsMovable(True)
        # self.hide_button.clicked.connect(self.hide_selected)
        # self.hide_all_button.clicked.connect(self.hide_all)
        # self.show_button.clicked.connect(self.show_hidden)
        # self.search.initialize('jobs_search_history',
        #         help_text=_('Search for a job by name'))
        # self.search.search.connect(self.find)
        # self.search_button.clicked.connect(lambda :
        #         self.find(self.search.current_text))
        # self.clear_button.clicked.connect(lambda : self.search.clear())
        self.restore_state()

    def restore_state(self):
        # try:
        #     geom = gprefs.get('jobs_dialog_geometry', bytearray(''))
        #     self.restoreGeometry(QByteArray(geom))
        #     state = gprefs.get('jobs view column layout3', None)
        #     if state is not None:
        #         self.jobs_view.horizontalHeader().restoreState(QByteArray(state))
        # except:
        #     pass
        # idx = self.jobs_view.model().index(0, 0)
        # if idx.isValid():
        #     sm = self.jobs_view.selectionModel()
        #     sm.select(idx, sm.ClearAndSelect|sm.Rows)
        pass

    def save_state(self):
        # try:
        #     state = bytearray(self.jobs_view.horizontalHeader().saveState())
        #     gprefs['jobs view column layout3'] = state
        #     geom = bytearray(self.saveGeometry())
        #     gprefs['jobs_dialog_geometry'] = geom
        # except:
        #     pass
        pass

    def show_job_details(self, index):
        # index = self.proxy_model.mapToSource(index)
        # if index.isValid():
        #     row = index.row()
        #     job = self.model.row_to_job(row)
        #     d = DetailView(self, job)
        #     d.exec_()
        #     d.timer.stop()
        pass

    def show_details(self, *args):
        index = self.jobs_view.currentIndex()
        if index.isValid():
            self.show_job_details(index)

    def kill_job(self, *args):
        # indices = [self.proxy_model.mapToSource(index) for index in
        #         self.jobs_view.selectionModel().selectedRows()]
        # indices = [i for i in indices if i.isValid()]
        # rows = [index.row() for index in indices]
        # if not rows:
        #     return error_dialog(self, _('No job'),
        #         _('No job selected'), show=True)
        # if question_dialog(self, _('Are you sure?'),
        #         ngettext('Do you really want to stop the selected job?',
        #             'Do you really want to stop all the selected jobs?',
        #             len(rows))):
        #     if len(rows) > 1:
        #         self.model.kill_multiple_jobs(rows, self)
        #     else:
        #         self.model.kill_job(rows[0], self)
        pass

    def kill_all_jobs(self, *args):
        # if question_dialog(self, _('Are you sure?'),       # TODO question_dialog
        #         _('Do you really want to stop all non-device jobs?')):
        #     self.model.kill_all_jobs()
        pass

    def hide_selected(self, *args):
        # indices = [self.proxy_model.mapToSource(index) for index in
        #         self.jobs_view.selectionModel().selectedRows()]
        # indices = [i for i in indices if i.isValid()]
        # rows = [index.row() for index in indices]
        # if not rows:
        #     return error_dialog(self, _('No job'),
        #         _('No job selected'), show=True)
        # self.model.hide_jobs(rows)
        # self.proxy_model.beginResetModel(), self.proxy_model.endResetModel()
        pass

    def hide_all(self, *args):
        self.model.hide_jobs(list(xrange(0,
            self.model.rowCount(QModelIndex()))))
        self.proxy_model.beginResetModel(), self.proxy_model.endResetModel()

    def show_hidden(self, *args):
        self.model.show_hidden_jobs()
        self.find(self.search.current_text)

    def closeEvent(self, e):
        self.save_state()
        return QDialog.closeEvent(self, e)

    def show(self, *args):
        self.restore_state()
        return QDialog.show(self, *args)

    def hide(self, *args):
        self.save_state()
        return QDialog.hide(self, *args)

    def reject(self):
        self.save_state()
        QDialog.reject(self)

    def find(self, query):
        self.proxy_model.find(query)


if __name__ == '__main__':
    from PyQt4.Qt import QApplication
    app = QApplication([])
    d = JobsDialog()
    d.exec_()
    del app