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

import logger
import misc
import note

@logger.logFn
def chooseNotebook(notebook_mvc, a_notebook = None):
    """
    Prompts the user to choose a NotebookStandardItem from either:
      (1) The currently selected NotebookStandardItems or 
      (2) All of the the NotebookStandardItems if none are selected.
    
    If only one NotebookStandardItem is selected that will be returned
    immediately without opening a dialog.

    Returns the choosen NotebookStandardItem (or None).
    """
    if a_notebook is None:
        notebooks = notebook_mvc.getSelectedNotebooks()
    else:
        notebooks = notebook_mvc.getAllNotebooks()
        notebooks.remove(a_notebook)
        
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
    

class NotebookChooser(QtGui.QDialog):
    """
    Dialog for choosing a NotebookStandardItem from a list of NotebookStandardItems.
    """
    @logger.logFn
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

    @logger.logFn
    def handleClick(self, index):
        source_index = self.proxy_model.mapToSource(index)
        self.choosen = self.model.itemFromIndex(source_index).notebook_item

    @logger.logFn        
    def handleDoubleClick(self, index):
        self.handleClick(index)
        self.accept()
        

class NotebookListViewDelegate(QtGui.QStyledItemDelegate):
    """
    A custom look for each notebook item.
    """
    def __init__(self, model, proxy_model):
        QtGui.QStyledItemDelegate.__init__(self)
        self.model = model
        self.proxy_model = proxy_model

    def itemFromProxyIndex(self, proxy_index):
        source_index = self.proxy_model.mapToSource(proxy_index)
        return self.model.itemFromIndex(source_index)
    
    def paint(self, painter, option, index):
        notebook = self.itemFromProxyIndex(index)

        # Draw correct background.
        style = option.widget.style()
        style.drawControl(QtGui.QStyle.CE_ItemViewItem, option, painter, option.widget)

        # Draw text.
        #if notebook.getUnpushed():
        #    painter.setPen(QtGui.QColor(100,0,0))
        #else:
        #    painter.setPen(QtGui.QColor(0,100,0))
        if notebook.getUnpushed():
            painter.drawText(option.rect, QtCore.Qt.AlignLeft, " " + notebook.getName() + "*")
        else:
            painter.drawText(option.rect, QtCore.Qt.AlignLeft, " " + notebook.getName())            
        painter.drawText(option.rect, QtCore.Qt.AlignRight, "(" + str(notebook.getNumberNotes()) + " notes) ")

        
class NotebookMVC(QtGui.QListView):
    """
    Encapsulates a list view specialized for notebooks and it's associated model.
    """
    addNewNote = QtCore.pyqtSignal(object)
    addNewNotebook = QtCore.pyqtSignal()
    selectedNotebooksChanged = QtCore.pyqtSignal(list)

    @logger.logFn    
    def __init__(self, parent = None):
        QtGui.QListView.__init__(self, parent)
        self.right_clicked = None

        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        # Context menu
        self.addNoteAction = QtGui.QAction(self.tr("Add Note"), self)
        self.addNoteAction.triggered.connect(self.handleAddNewNote)
        self.addNotebookAction = QtGui.QAction(self.tr("New Notebook"), self)
        self.addNotebookAction.triggered.connect(self.handleAddNewNotebook)
        self.renameNotebookAction = QtGui.QAction(self.tr("Rename"), self)
        self.renameNotebookAction.triggered.connect(self.handleRenameNotebook)
        self.deleteAction = QtGui.QAction(self.tr("Delete Notebook"), self)
        self.deleteAction.triggered.connect(self.handleDelete)
        self.nb_popup_menu = QtGui.QMenu(self)
        self.nb_popup_menu.addAction(self.addNoteAction)
        self.nb_popup_menu.addAction(self.addNotebookAction)
        self.nb_popup_menu.addAction(self.deleteAction)
        self.nb_popup_menu.addAction(self.renameNotebookAction)        
        self.no_nb_popup_menu = QtGui.QMenu(self)
        self.no_nb_popup_menu.addAction(self.addNotebookAction)

        # Notebook model
        self.notebook_model = NotebookStandardItemModel(self)
        self.notebook_proxy_model = NotebookSortFilterProxyModel(self)
        self.notebook_proxy_model.setSourceModel(self.notebook_model)
        self.setModel(self.notebook_proxy_model)

        # Rendering
        self.setItemDelegate(NotebookListViewDelegate(self.notebook_model, self.notebook_proxy_model))
        
        # Get selection changes.
        self.selectionModel().selectionChanged.connect(self.handleSelectionChange)

    @logger.logFn        
    def addNotebook(self, directory, notebook_name, username, email):
        nb = NotebookStandardItem(directory)
        nb.createWithName(notebook_name, username, email)
        self.notebook_model.appendRow(nb)
        self.notebook_proxy_model.sort(0)

    @logger.logFn
    def clearNotebooks(self):
        self.notebook_model.clear()

    @logger.logFn        
    def getAllNotebooks(self):
        all_notebooks = []
        for row in range(self.notebook_model.rowCount()):
            index = self.notebook_model.index(row, 0)
            all_notebooks.append(self.notebook_model.itemFromIndex(index))
        return all_notebooks

    @logger.logFn    
    def getSelectedNotebooks(self):
        selected_notebooks = []
        for index in self.selectedIndexes():
            selected_notebooks.append(self.notebookFromProxyIndex(index))
        return selected_notebooks

    @logger.logFn    
    def handleAddNewNote(self, boolean):
        self.addNewNote.emit(self.notebookFromProxyIndex(self.right_clicked))

    @logger.logFn
    def handleAddNewNotebook(self, boolean):
        self.addNewNotebook.emit()

    @logger.logFn        
    def handleDelete(self, boolean):
        notebook = self.notebookFromProxyIndex(self.right_clicked)
        notebook_name = notebook.getName()

        reply = QtGui.QMessageBox.question(self,
                                           "Warning!",
                                           "Really delete notebook '" + notebook_name + "'?",
                                           QtGui.QMessageBox.Yes,
                                           QtGui.QMessageBox.No)
        if (reply == QtGui.QMessageBox.Yes):
            source_index = self.notebook_proxy_model.mapToSource(self.right_clicked)
            self.notebook_model.removeRow(source_index.row())

            # This just renames the notebook.xml file to deleted.xml so that
            # it won't be found the next time the program is started.
            notebook.deleteNotebook()

    @logger.logFn
    def handleRenameNotebook(self, boolean):
        notebook = self.notebookFromProxyIndex(self.right_clicked)
        notebook_name = notebook.getName()
        [new_name, ok] = QtGui.QInputDialog.getText(self,
                                                    'Rename Notebook',
                                                    'Enter a new name:',
                                                    text = notebook_name)
        if ok:
            notebook.rename(new_name)
            self.notebook_proxy_model.sort(0)
    
    @logger.logFn            
    def handleSelectionChange(self, new_item_selection, old_item_selection):
        selected_notebooks = self.getSelectedNotebooks()
        if (len(selected_notebooks) > 0):
            self.selectedNotebooksChanged.emit(selected_notebooks)

    @logger.logFn            
    def loadNotebooks(self, directory):
        self.clearNotebooks()

        for nb_id in map(lambda(x): x[len(directory) + 3:], glob.glob(directory + "nb_*")):
            nb = NotebookStandardItem(directory)
            if nb.loadWithUUID(nb_id):
                self.notebook_model.appendRow(nb)

        self.notebook_proxy_model.sort(0)

    @logger.logFn        
    def mousePressEvent(self, event):
        if (event.button() == QtCore.Qt.RightButton):
            self.right_clicked = self.indexAt(event.pos())
            if (self.right_clicked.row() > -1):
                self.nb_popup_menu.exec_(event.globalPos())
            else:
                self.no_nb_popup_menu.exec_(event.globalPos())                
        else:
            QtGui.QListView.mousePressEvent(self, event)

    @logger.logFn        
    def notebookFromProxyIndex(self, proxy_index):
        source_index = self.notebook_proxy_model.mapToSource(proxy_index)
        return self.notebook_model.itemFromIndex(source_index)


class NotebookSortFilterProxyModel(QtGui.QSortFilterProxyModel):
    """
    Sort notebooks.
    """

    
class NotebookStandardItem(QtGui.QStandardItem):
    """
    A single notebook in the notebook listview model.
    """
    @logger.logFn
    def __init__(self, directory):
        """
        After creating the item you need to enter the appropriate initial
        data using one of createWithName() or loadWithUUID.
        """
        QtGui.QStandardItem.__init__(self, "NA")

        self.directory = directory + "nb_"
        self.git_log = []
        self.has_unpushed = False
        self.name = None
        self.number_notes = 0
        self.number_unsaved = 0
        self.uuid = None

    @logger.logFn        
    def createWithName(self, notebook_name, username, email):
        self.name = notebook_name
        self.uuid = str(uuid.uuid1())
        self.setText(self.name)

        self.directory += self.uuid
        os.makedirs(self.directory)

        xml = ElementTree.Element("notebook")
        name_xml = ElementTree.SubElement(xml, "name")
        name_xml.text = self.name

        self.directory += "/"
        misc.pSaveXML(self.directory + "notebook.xml", xml)

        # Create a new git repository for this notebook.
        misc.gitInit(self.directory, username, email)

        # Commit the notebook name.
        misc.gitAddCommit(self.directory, self.directory + "notebook.xml", "add notebook.")

        self.has_unpushed = True

    @logger.logFn
    def deleteNotebook(self):
        os.rename(self.directory + "notebook.xml", self.directory + "deleted.xml")
        
    @logger.logFn        
    def decNumberUnsaved(self):
        self.number_unsaved -= 1
        if (self.number_unsaved == 0):
            self.setForeground(QtGui.QBrush(QtGui.QColor(0,0,0)))

    @logger.logFn            
    def getDirectory(self):
        return self.directory

    @logger.logFn    
    def getName(self):
        return self.name

    @logger.logFn    
    def getNoteVersions(self, note_filename):
        versions = []
        for commit in self.git_log:
            if (commit[2] == note_filename):
                versions.append(commit[0])
        return list(reversed(versions))

    def getNumberNotes(self):
        return self.number_notes

    @logger.logFn
    def getUnpushed(self):
        return self.has_unpushed
    
    @logger.logFn
    def incNumberNotes(self, inc):
        self.number_notes += inc
        
    @logger.logFn
    def incNumberUnsaved(self):
        self.number_unsaved += 1
        self.setForeground(QtGui.QBrush(QtGui.QColor(100,0,0)))

    @logger.logFn        
    def loadWithUUID(self, notebook_uuid):
        self.uuid = notebook_uuid
        self.directory = self.directory + self.uuid + "/"
        if os.path.exists(self.directory + "notebook.xml"):
            xml = ElementTree.parse(self.directory + "notebook.xml").getroot()
            self.name = xml.find("name").text
            self.setText(self.name)

            self.git_log = misc.gitGetLog(self.directory)
            self.has_unpushed = misc.gitHasUnpushed(self.directory)
            
            return True
        else:
            return False

    @logger.logFn
    def rename(self, new_name):
        self.name = str(new_name)
        self.setText(new_name)
        
        # Update the XML and commit.
        xml = ElementTree.Element("notebook")
        name_xml = ElementTree.SubElement(xml, "name")
        name_xml.text = self.name

        misc.pSaveXML(self.directory + "notebook.xml", xml)
        misc.gitAddCommit(self.directory, self.directory + "notebook.xml", "rename notebook.")

        self.setUnpushed()

    @logger.logFn
    def setNumberNotes(self, number_notes):
        self.number_notes = number_notes

    @logger.logFn
    def setUnpushed(self):
        self.has_unpushed = True
        self.emitDataChanged()
        

class NotebookStandardItemModel(QtGui.QStandardItemModel):
    """
    The notebook listview model.
    """

    
