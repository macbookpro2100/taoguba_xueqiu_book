#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

HORIZONTAL_HEADERS = (u"website", u"info")


class Recipes(object):
    u"""

    """
    def __init__(self, url, recipe_info, lang):
        self.url = url
        self.recipe_info = recipe_info
        self.lang = lang

    def __repr__(self):
        return "%s" % self.url


class TreeItem(object):
    u"""
    a python object used to return row/column data, and keep note of
    it's parents and/or children
    """
    def __init__(self, recipe, header, parent_item):
        self.recipe = recipe
        self.parent_item = parent_item
        self.header = header
        self.childItems = []

    def append_child(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return 2            # TODO 解决硬编码的问题

    def data(self, column):
        if self.recipe is None:
            if column == 0:
                return QtCore.QVariant(self.header)
            if column == 1:
                return QtCore.QVariant("")
        else:
            if column == 0:
                return QtCore.QVariant(self.recipe.url)
            if column == 1:
                return QtCore.QVariant(self.recipe.recipe_info)
        return QtCore.QVariant()

    def parent(self):
        return self.parent_item

    def row(self):
        if self.parent_item:
            return self.parent_item.childItems.index(self)
        return 0


class RecipeModel(QtCore.QAbstractItemModel):
    u"""
    a model to display a few names
    """
    def __init__(self, parent=None):
        super(RecipeModel, self).__init__(parent)
        self.recipe = []
        for url, recipe_info, lang in (
                ("zhihu", u"问题, 答案, 专栏", u"Chinese"),
                ("jianshu", u"文章", u"Chinese"),
                ("sinablog", u"博客", u"Chinese")
        ):
            recipe_item = Recipes(url, recipe_info, lang)
            self.recipe.append(recipe_item)

        self.rootItem = TreeItem(None, "ALL", None)
        self.parents = {0: self.rootItem}
        self.setupModelData()

    def columnCount(self, recipe=None):
        if recipe and recipe.isValid():
            return recipe.internalPointer().columnCount()
        else:
            return len(HORIZONTAL_HEADERS)

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()

        item = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            return item.data(index.column())
        if role == QtCore.Qt.UserRole:
            if item:
                return item.recipe

        return QtCore.QVariant()

    def headerData(self, column, orientation, role):
        if (orientation == QtCore.Qt.Horizontal and
        role == QtCore.Qt.DisplayRole):
            try:
                return QtCore.QVariant(HORIZONTAL_HEADERS[column])
            except IndexError:
                pass

        return QtCore.QVariant()

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parent_item = self.rootItem
        else:
            parent_item = parent.internalPointer()

        childItem = parent_item.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        if not childItem:
            return QtCore.QModelIndex()

        parent_item = childItem.parent()

        if parent_item == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            p_item = self.rootItem
        else:
            p_item = parent.internalPointer()
        return p_item.childCount()

    def setupModelData(self):
        for item in self.recipe:
            lang = item.lang

            if lang not in self.parents:
                new_parent = TreeItem(None, lang, self.rootItem)
                self.rootItem.append_child(new_parent)

                self.parents[lang] = new_parent

            parent_item = self.parents[lang]
            newItem = TreeItem(item, "", parent_item)
            parent_item.append_child(newItem)

    def search_model(self, recipe):
        u"""
        get the modelIndex for a given appointment
        :param recipe:
        :return:
        """
        def search_node(node):
            u"""
             a function called recursively, looking at all nodes beneath node
            :param node:
            :return:
            """
            for child in node.childItems:
                if recipe == child.recipe:
                    index = self.createIndex(child.row(), 0, child)
                    return index

                if child.childCount() > 0:
                    child_result = search_node(child)
                    if child_result:
                        return child_result

        result = search_node(self.parents[0])
        return result

    def find_given_name(self, url):
        app = None
        for item in self.recipe:
            if item.url == url:
                app = item
                break
        if app is not None:
            index = self.search_model(app)
            return True, index
        return False, None

