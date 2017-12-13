#!/usr/bin/env python
"""
.. module:: keywords
   :synopsis: keywords chooser and editor dialogs.
"""

import os
import shutil
import uuid

from PyQt5 import QtCore, QtGui, QtWidgets

import logger


class KeywordChooserMVC(QtWidgets.QListView):
    """
    Encapsulates a list view specialized for selecting keywords. This is
    where the user can select key words to use to filter the notes.

    A reference counting scheme is used to key track of how many notes
    contain a particular keyword. If this count reaches zero the keyword 
    is removed.
    """
    selectedKeywordsChanged = QtCore.pyqtSignal(list)
    
    @logger.logFn
    def __init__(self, parent = None):
        super().__init__(parent)

        self.all_keywords = {}
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        # Keyword chooser model
        self.keyword_chooser_model = QtGui.QStandardItemModel(self)
        self.setModel(self.keyword_chooser_model)

        # Get selection changes.
        self.selectionModel().selectionChanged.connect(self.handleSelectionChange)
        
    @logger.logFn
    def addKeyword(self, keyword):
        if keyword in self.all_keywords:
            self.all_keywords[keyword].incCount()
        else:
            keyword_item = KeywordChooserStandardItem(keyword)
            self.all_keywords[keyword] = keyword_item
            self.keyword_chooser_model.appendRow(keyword_item)
            self.keyword_chooser_model.sort(0)

    @logger.logFn
    def deleteKeyword(self, keyword):
        keyword_item = self.all_keywords[keyword]
        if (keyword_item.decCount() == 0):
            self.keyword_chooser_model.removeRow(self.keyword_chooser_model.indexFromItem(keyword_item).row())
            del self.all_keywords[keyword]

    @logger.logFn
    def getAllKeywords(self):
        return self.all_keywords.keys()
            
    @logger.logFn            
    def handleSelectionChange(self, new_item_selection, old_item_selection):
        keywords = []
        for index in self.selectedIndexes():
            keyword_item = self.keyword_chooser_model.itemFromIndex(index)
            keywords.append(str(keyword_item.text()))
        self.selectedKeywordsChanged.emit(keywords)

    @logger.logFn
    def updateKeywords(self, old_keywords, new_keywords):

        # Delete only the keywords that are not also in the new list.
        to_del = [x for x in old_keywords if not x in new_keywords]
        for d in to_del:
            self.deleteKeyword(d)

        # Add only the keywords that are not also in the old list.
        to_add = [x for x in new_keywords if not x in old_keywords]
        for a in to_add:
            self.addKeyword(a)


class KeywordChooserStandardItem(QtGui.QStandardItem):
    """
    A single keyword that the user can click on to select.
    """
    @logger.logFn
    def __init__(self, keyword):
        super().__init__(keyword)

        self.setEditable(False)
        self.ref_counts = 1

    @logger.logFn
    def incCount(self):
        self.ref_counts += 1

    @logger.logFn
    def decCount(self):
        self.ref_counts -= 1
        return self.ref_counts

    
class KeywordEditorMVC(QtWidgets.QListView):
    """
    Encapsulates a list view specialized for adding and removing
    keywords from a specific note.
    """
    #selectedKeywordChanged = QtCore.pyqtSignal(object)

    @logger.logFn
    def __init__(self, parent = None):
        super().__init__(parent)

        self.keywords = []
        self.right_clicked = None

        # Context menu
        self.deleteKeywordAction = QtWidgets.QAction(self.tr("Delete Keyword"), self)
        self.deleteKeywordAction.triggered.connect(self.handleDeleteKeyword)

        self.popup_menu = QtWidgets.QMenu(self)
        self.popup_menu.addAction(self.deleteKeywordAction)
        
        # Keyword editor model.
        self.keyword_editor_model = QtGui.QStandardItemModel(self)
        self.setModel(self.keyword_editor_model)

    @logger.logFn
    def addKeyword(self, keyword):
        if not keyword in self.keywords:
            self.keywords.append(keyword)
            kw_item = QtGui.QStandardItem(keyword)
            kw_item.setEditable(False)
            self.keyword_editor_model.appendRow(kw_item)
            self.keyword_editor_model.sort(0)

    @logger.logFn
    def addKeywords(self, keywords):
        for keyword in keywords:
            self.addKeyword(keyword)
        
    @logger.logFn
    def getAllKeywords(self):
        return list(self.keywords)
        
    @logger.logFn
    def handleDeleteKeyword(self, boolean):
        self.keywords.remove(str(self.keyword_editor_model.itemFromIndex(self.right_clicked).text()))
        self.keyword_editor_model.removeRow(self.right_clicked.row())

    @logger.logFn        
    def mousePressEvent(self, event):
        if (event.button() == QtCore.Qt.RightButton):
            self.right_clicked = self.indexAt(event.pos())
            if (self.right_clicked.row() > -1):
                self.popup_menu.exec_(event.globalPos())
