#!/usr/bin/env python
"""
.. module:: notebook
   :synopsis: The Notebook class and related classes.
"""

import glob
import os
import uuid

from xml.etree import ElementTree

from PyQt4 import QtCore, QtGui

import notebook_chooser_ui as notebookChooserUi

import misc
import note


def chooseNotebook(notebook_mvc):
    """
    Prompts the user to choose a NotebookStandardItem from either:
      (1) The currently selected NotebookStandardItems or 
      (2) All of the the NotebookStandardItems if none are selected.
    
    If only one NotebookStandardItem is selected that will be returned
    immediately without opening a dialog.

    Returns the choosen NotebookStandardItem (or None).
    """
    notebooks = notebook_mvc.getSelectedNotebooks()
    if (len(notebooks) == 0):
        notebooks = notebook_mvc.getAllNotebooks()
    if (len(notebooks) == 1):
        return notebooks[0]
    else:
        dialog = NotebookChooser(notebooks)
        if dialog.exec_():
            return dialog.choosen
        else:
            return None
    

#
# FIXME:
#  1. Merge with NotebookStandardItem?
#  2. Move all file related stuff here.
#
class Notebook(object):
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
        self.notes = []

        # Load an old notebook.
        if nb_uuid is not None:
            self.uuid = nb_uuid
            self.directory = self.directory + self.uuid + "/"
            xml = ElementTree.parse(self.directory + "notebook.xml").getroot()
            self.name = xml.find("name").text

            # Load notes.
            for n_id in map(lambda(x): x[len(self.directory):-4], glob.glob(self.directory + "*.xml")):
                if not (n_id == "notebook"):
                    print "found:", n_id
                #self.notes.append(note.Note(self.directory, uuid = n_id))
            
        # Create a new notebook.
        else:
            self.name = nb_name
            self.notes = []
            self.uuid = str(uuid.uuid1())

            self.directory += self.uuid
            os.makedirs(self.directory)

            xml = ElementTree.Element("notebook")
            name_xml = ElementTree.SubElement(xml, "name")
            name_xml.text = self.name

            self.directory += "/"
            misc.pSaveXML(self.directory + "notebook.xml", xml)

            # Create a new git repository for this notebook.

    def getDirectory(self):
        return self.directory
    
    def getName(self):
        return self.name


class NotebookChooser(QtGui.QDialog):
    """
    Dialog for choosing a NotebookStandardItem from a list of NotebookStandardItems.
    """
    def __init__(self, notebook_items = [], parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.choosen = None

        self.ui = notebookChooserUi.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Notebook Chooser")
        
        self.model = QtGui.QStandardItemModel()
        self.proxy_model = QtGui.QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.ui.chooserListView.setModel(self.proxy_model)

        #
        # Hm, apparently we can't use the same items in two different models,
        # so we have to do some fiddling..
        #
        for nb in notebook_items:
            item = QtGui.QStandardItem(nb.getName())
            item.notebook_item = nb
            self.model.appendRow(item)
            
        self.proxy_model.sort(0)

        self.ui.chooserListView.clicked.connect(self.handleClick)
        self.ui.chooserListView.doubleClicked.connect(self.handleDoubleClick)

    def handleClick(self, index):
        source_index = self.proxy_model.mapToSource(index)
        self.choosen = self.model.itemFromIndex(source_index).notebook_item

    def handleDoubleClick(self, index):
        self.handleClick(index)
        self.accept()
        

class NotebookMVC(QtGui.QListView):
    """
    Encapsulates a list view specialized for notebooks and it's associated model.
    """
    selectedNotesChanged = QtCore.pyqtSignal(list)
    
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
        self.notebook_model = NotebookStandardItemModel()
        self.notebook_proxy_model = NotebookSortFilterProxyModel()
        self.notebook_proxy_model.setSourceModel(self.notebook_model)
        self.setModel(self.notebook_proxy_model)
        
    def addNotebook(self, directory, name):
        nb = Notebook(directory, nb_name = name)
        self.notebook_model.appendRow(NotebookStandardItem(nb))
        self.notebook_proxy_model.sort(0)

    def clearNotebooks(self):
        self.notebook_model.clear()

    def getAllNotebooks(self):
        all_notebooks = []
        for row in range(self.notebook_model.rowCount()):
            index = self.notebook_model.index(row, 0)
            all_notebooks.append(self.notebook_model.itemFromIndex(index))
        return all_notebooks

    def getSelectedNotebooks(self):
        selected_notebooks = []
        for index in self.selectedIndexes():
            source_index = self.notebook_proxy_model.mapToSource(index)
            selected_notebooks.append(self.notebook_model.itemFromIndex(source_index))
        return selected_notebooks
        
    def loadNotebooks(self, directory):
        self.clearNotebooks()

        for nb_id in map(lambda(x): x[len(directory) + 3:], glob.glob(directory + "nb_*")):
            self.notebook_model.appendRow(NotebookStandardItem(Notebook(directory, nb_uuid = nb_id)))

        self.notebook_proxy_model.sort(0)

    def handleDelete(self, boolean):
        source_index = self.notebook_proxy_model.mapToSource(self.right_clicked)
        notebook = self.notebook_model.itemFromIndex(source_index)
        notebook_name = notebook.getNotebook().getName()

        reply = QtGui.QMessageBox.question(self,
                                           "Warning!",
                                           "Really delete notebook '" + notebook_name + "'?",
                                           QtGui.QMessageBox.Yes,
                                           QtGui.QMessageBox.No)
        if (reply == QtGui.QMessageBox.Yes):
            self.notebook_model.removeRow(source_index.row())
    
    def mousePressEvent(self, event):
        if (event.button() == QtCore.Qt.RightButton):
            self.right_clicked = self.indexAt(event.pos())
            if (self.right_clicked.row() > -1):
                self.popup_menu.exec_(event.globalPos())
        else:
            QtGui.QListView.mousePressEvent(self, event)

#    def mouseReleaseEvent(self, event):
#        if (event.button() == QtCore.Qt.LeftButton):
#            selected_notes = []
#            for index in self.selectedIndexes():
#                source_index = self.notebook_proxy_model.mapToSource(index)
#                selected_notebooks.append(self.notebook_model.itemFromIndex(source_index))
#                print index.row()
        
        
class NotebookSortFilterProxyModel(QtGui.QSortFilterProxyModel):
    """
    Sorts so that the "All" notebook is always first.
    """
#    def lessThan(self, left, right):
#        nb1 = self.sourceModel().itemFromIndex(left).getNoteBook()
#        nb2 = self.sourceModel().itemFromIndex(right).getNoteBook()
#        if (nb1.getName() == "All"):
#            return True
#        else:
#            return True if(nb1.getName() < nb2.getName()) else False


class NotebookStandardItem(QtGui.QStandardItem):
    """
    Store a single notebook in the notebook listview model.
    """
    def __init__(self, notebook):
        QtGui.QStandardItem.__init__(self, notebook.getName())
        self.notebook = notebook
        self.number_unsaved = 0

    def decNumberUnsaved(self):
        self.number_unsaved -= 1
        if (self.number_unsaved == 0):
            self.setForeground(QtGui.QBrush(QtGui.QColor(0,0,0)))

    def getDirectory(self):
        return self.notebook.getDirectory()
    
    def getName(self):
        return self.notebook.getName()
    
    def getNotebook(self):
        return self.notebook

    def incNumberUnsaved(self):
        self.number_unsaved += 1
        self.setForeground(QtGui.QBrush(QtGui.QColor(100,0,0)))


class NotebookStandardItemModel(QtGui.QStandardItemModel):
    """
    The notebook listview model.
    """
    def __init__(self, parent = None):
        QtGui.QStandardItemModel.__init__(self, parent)

    
