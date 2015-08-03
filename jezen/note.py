#!/usr/bin/env python
"""
.. module:: note
   :synopsis: The Note class.
"""

import glob
import os
import uuid

from PyQt4 import QtCore, QtGui

from xml.etree import ElementTree

import misc


class NoteMVC(QtGui.QListView):
    """
    Encapsulates a list view specialized for notes and it's associated model.
    """
    selectedNoteChanged = QtCore.pyqtSignal(object)

    def __init__(self, parent = None):
        QtGui.QListView.__init__(self, parent)

        # Note model
        self.note_model = NoteStandardItemModel()
        self.note_proxy_model = NoteSortFilterProxyModel()
        self.note_proxy_model.setSourceModel(self.note_model)
        self.setModel(self.note_proxy_model)

        # Get selection changes.
        self.selectionModel().selectionChanged.connect(self.handleSelectionChange)
        
    def addNote(self, notebook, name):
        """
        Add a new blank note.
        """
        self.note_model.appendRow(NoteStandardItem(notebook, note_name = name))
        self.note_proxy_model.sort(0)

    def clearNotes(self):
        self.note_model.clear()

    def handleSelectionChange(self, new_item_selection, old_item_selection):
        source_index = self.note_proxy_model.mapToSource(self.selectedIndexes()[0])
        self.selectedNoteChanged.emit(self.note_model.itemFromIndex(source_index))

    def loadNotes(self, notebook):
        """
        Loads all the notes in a notebook.
        """
        for n_file in glob.glob(notebook.getDirectory() + "note_*.xml"):
            self.note_model.appendRow(NoteStandardItem(notebook, note_file = n_file))

        self.note_proxy_model.sort(0)

    def updateNotebookFilter(self, notebooks):
        self.note_proxy_model.setNotebooks(notebooks)
        self.note_proxy_model.sort(0)
        
#    def mousePressEvent(self, event):
#        if (event.button() == QtCore.Qt.RightButton):
#            self.right_clicked = self.indexAt(event.pos())
#            if (self.right_clicked.row() > -1):
#                self.popup_menu.exec_(event.globalPos())
#        else:
#            QtGui.QListView.mousePressEvent(self, event)


class NoteSortFilterProxyModel(QtGui.QSortFilterProxyModel):
    """
    Sort and filter notes. At the start (or when changing directories) we
    load all the notes, but only show the ones that match the filters.
    """
    def __init__(self, parent = None):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        self.keywords = []
        self.notebooks = []

    def filterAcceptsRow(self, source_row, source_parent):
        index = self.sourceModel().index(source_row, 0, source_parent)
        note = self.sourceModel().itemFromIndex(index)
        accept = False
        if (note.getNotebook() in self.notebooks):
            accept = True

        return accept

    def setNotebooks(self, new_notebooks):
        self.notebooks = new_notebooks
        self.invalidateFilter()
    
    
class NoteStandardItem(QtGui.QStandardItem):
    """
    A single note.

    This class also handles loading and saving notes.
    """
    def __init__(self, notebook, note_file = None, note_name = None):
        """
        Load on old note (when given a note_file), or create a
        new note (when given a name).

        notebook is a NotebookStandardItem.

        note_file is path/note_(uuid).xml
        """
        self.notebook = notebook
        self.unsaved_markdown = None

        # Load an old note.
        if note_file is not None:
            self.fullname = note_file
            self.filename = os.path.basename(self.fullname)
            xml = ElementTree.parse(self.fullname).getroot()
            self.markdown = xml.find("markdown").text
            self.name = xml.find("name").text

        # Create a new note.
        else:
            self.markdown = ""
            self.name = note_name
            self.filename = "note_" + str(uuid.uuid1()) + ".xml"
            self.fullname = self.notebook.getDirectory() + self.filename
            
        QtGui.QStandardItem.__init__(self, self.name)

    def copyNote(self, notebook):
        """
        Return a copy with a different uuid and possibly a different notebook.

        notebook is a NotebookStandartItem.
        """
        pass

    def deleteNote(self):
        """
        Remove the note file from the disk and create a git commit.
        """
        pass

    def getMarkdown(self):
        return self.markdown
    
    def getName(self):
        return self.name

    def getNotebook(self):
        return self.notebook

    def getUnsavedMarkdown(self):
        return self.unsaved_markdown

    def moveNote(self, new_notebook):
        """
        Notebooks are just directories, so update the filename accordingly.

        new_notebook is a NotebookStandardItem.
        """
        self.notebook = new_notebook
        self.filename = self.notebook.getDirectory() + self.uuid

    def saveBackup(self):
        backup_name = self.fullname[:-4] + "_backup.txt"
        with open(backup_name, "w") as fp:
            fp.write(self.markdown)
        
    def saveNote(self):
        """
        Save XML and create a git commit.
        """

        # Save XML.
        xml = ElementTree.Element("note")
        
        name_xml = ElementTree.SubElement(xml, "name")
        name_xml.text = self.name
        
        markdown_xml = ElementTree.SubElement(xml, "markdown")
        markdown_xml.text = self.markdown

        misc.pSaveXML(self.fullname, xml)

        # Delete backup.
        
        # git commit.

    def setMarkdown(self, new_markdown):
        self.markdown = new_markdown

    def setUnsavedMarkdown(self, new_markdown):
        self.unsaved_markdown = new_markdown
        
        
class NoteStandardItemModel(QtGui.QStandardItemModel):
    """
    The note listview model.
    """
    def __init__(self, parent = None):
        QtGui.QStandardItemModel.__init__(self, parent)

    
