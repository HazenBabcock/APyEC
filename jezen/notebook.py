#!/usr/bin/env python
"""
.. module:: notebook
   :synopsis: The NoteBook class.
"""

import os
import uuid

from xml.etree import ElementTree

from PyQt4 import QtCore, QtGui

import misc


class NoteBook(object):
    """
    This class is the interface between notebooks on the disk
    and what is displayed.
    """
    def __init__(self, directory, nb_uuid = None, nb_name = None):
        """
        Load on old notebook (when given a uuid), or create a
        new notebook (when given a name).
        
        Note: The uuid is the directory that the notebook is stored in.
        """
        self.directory = directory + "nb_"

        # Load an old notebook.
        if nb_uuid is not None:
            self.uuid = nb_uuid
            xml = ElementTree.parse(self.directory + self.uuid + "/notebook.xml").getroot()
            self.name = xml.find("name").text

            # Load notes.
            
        # Create a new notebook.
        else:
            self.name = nb_name
            self.notes = []
            self.uuid = str(uuid.uuid1())

            os.makedirs(self.directory + self.uuid)

            xml = ElementTree.Element("notebook")
            name_xml = ElementTree.SubElement(xml, "name")
            name_xml.text = self.name

            misc.pSaveXML(self.directory + self.uuid + "/notebook.xml", xml)

            # Create a new git repository for this notebook.

    def getDirectory(self):
        return self.directory
    
    def getName(self):
        return self.name


class NoteBookMVC(QtGui.QListView):
    """
    Encapsulates a list view and it's associated model.
    """
    def __init__(self, parent = None):
        QtGui.QListView.__init__(self, parent)
        self.right_clicked = None
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        # Context menu
        self.deleteAction = QtGui.QAction(self.tr("Delete"), self)
        self.deleteAction.triggered.connect(self.handleDelete)
        self.popup_menu = QtGui.QMenu(self)
        self.popup_menu.addAction(self.deleteAction)

        # Notebook model
        self.notebook_model = NoteBookStandardItemModel()
        self.notebook_proxy_model = NoteBookSortFilterProxyModel()
        self.notebook_proxy_model.setSourceModel(self.notebook_model)
        self.setModel(self.notebook_proxy_model)
        
    def addNotebook(self, notebook):
        self.notebook_model.appendRow(NoteBookStandardItem(nb))
        self.notebook_proxy_model.sort(0)

    def loadNotebooks(self, notebooks):
        self.clearNotebooks()
        
        for nb in notebooks:
            self.notebook_model.appendRow(NoteBookStandardItem(nb))
        self.notebook_proxy_model.sort(0)
        
    def clearNotebooks(self):
        self.notebook_model.clear()

    def handleDelete(self, boolean):
        source_index = self.notebook_proxy_model.mapToSource(self.right_clicked)
        notebook = self.notebook_model.itemFromIndex(source_index)
        notebook_name = notebook.getNoteBook().getName()

        reply = QtGui.QMessageBox.question(self,
                                           "Warning!",
                                           "Really delete notebook '" + notebook_name + "'?",
                                           QtGui.QMessageBox.Yes,
                                           QtGui.QMessageBox.No)
        if (reply == QtGui.QMessageBox.Yes):
            self.notebook_model.removeRow(source_index.row())
    
    def mousePressEvent(self, event):
        QtGui.QListView.mousePressEvent(self, event)
        if (event.button() == QtCore.Qt.RightButton):
            self.right_clicked = self.indexAt(event.pos())
            if (self.right_clicked.row() > 0):
                self.popup_menu.exec_(event.globalPos())

        
        
class NoteBookSortFilterProxyModel(QtGui.QSortFilterProxyModel):
    """
    Sorts so that the "All" notebook is always first.
    """
    def lessThan(self, left, right):
        nb1 = self.sourceModel().itemFromIndex(left).getNoteBook()
        nb2 = self.sourceModel().itemFromIndex(right).getNoteBook()
        if (nb1.getName() == "All"):
            return True
        else:
            return True if(nb1.getName() < nb2.getName()) else False


class NoteBookStandardItem(QtGui.QStandardItem):
    """
    Store a single notebook in the notebook listview model.
    """
    def __init__(self, notebook):
        QtGui.QStandardItem.__init__(self, notebook.getName())
        self.notebook = notebook

    def getNoteBook(self):
        return self.notebook
                 
    
class NoteBookStandardItemModel(QtGui.QStandardItemModel):
    """
    The notebook listview model.
    """
    def __init__(self, parent = None):
        QtGui.QStandardItemModel.__init__(self, parent)

    
