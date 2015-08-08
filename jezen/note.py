#!/usr/bin/env python
"""
.. module:: note
   :synopsis: The Note class.
"""

import datetime
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
        self.notes = {}
        self.right_clicked = None

        # Context menu
        self.copyLinkAction = QtGui.QAction(self.tr("Copy Link to Clipboard"), self)
        self.copyLinkAction.triggered.connect(self.handleCopyLink)
        self.copyNoteAction = QtGui.QAction(self.tr("Copy Note"), self)
        self.copyNoteAction.triggered.connect(self.handleCopyNote)
        self.deleteNoteAction = QtGui.QAction(self.tr("Delete Note"), self)
        self.deleteNoteAction.triggered.connect(self.handleDeleteNote)

        self.popup_menu = QtGui.QMenu(self)
        self.popup_menu.addAction(self.copyLinkAction)
        self.popup_menu.addAction(self.copyNoteAction)
        self.popup_menu.addAction(self.deleteNoteAction)
        
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
        a_note = NoteStandardItem(notebook, note_name = name)
        self.notes[a_note.getFileName()] = a_note
        self.note_model.appendRow(a_note)
        self.note_proxy_model.sort(0)

    def clearNotes(self):
        self.note_model.clear()

#    def handleClicked(self, proxy_index):
#        if (proxy_index.row() == self.selectedIndexes()[0].row()):
#            print "clicked", proxy_index.row(), self.selectedIndexes()[0].row()
        
    def handleCopyLink(self, boolean):
        clipboard = QtGui.QApplication.clipboard()
        a_note = self.noteFromProxyIndex(self.right_clicked)
        clipboard.setText("[" + a_note.getName() + "](" + a_note.getLink() + ")")

    def handleCopyNote(self, boolean):
        pass

    def handleDeleteNote(self, boolean):
        pass

    def handleNoteLinkClicked(self, note_filename, note_version):
        note_filename = str(note_filename)
        if note_filename in self.notes:
            a_note = self.notes[note_filename]
            a_note.loadNote(note_version)
            source_index = self.note_model.indexFromItem(a_note)
            filter_index = self.note_proxy_model.mapFromSource(source_index)
            if filter_index.isValid():
                self.setCurrentIndex(filter_index)
            else:
                self.clearSelection()
                self.selectedNoteChanged.emit(a_note)
        
    def handleSelectionChange(self, new_item_selection, old_item_selection):
        if (len(self.selectedIndexes()) > 0):
            self.selectedNoteChanged.emit(self.noteFromProxyIndex(self.selectedIndexes()[0]))

    def loadNotes(self, notebook):
        """
        Loads all the notes in a notebook.
        """
        for n_file in glob.glob(notebook.getDirectory() + "note_*.xml"):
            a_note = NoteStandardItem(notebook, note_file = n_file)
            self.notes[a_note.getFileName()] = a_note
            self.note_model.appendRow(a_note)

        self.note_proxy_model.sort(0)

    def noteFromProxyIndex(self, proxy_index):
        source_index = self.note_proxy_model.mapToSource(proxy_index)
        return self.note_model.itemFromIndex(source_index)
        
    def updateNotebookFilter(self, notebooks):
        self.note_proxy_model.setNotebooks(notebooks)
        self.note_proxy_model.sort(0)
        
    def mousePressEvent(self, event):
        if (event.button() == QtCore.Qt.RightButton):
            self.right_clicked = self.indexAt(event.pos())
            if (self.right_clicked.row() > -1):
                self.popup_menu.exec_(event.globalPos())
        else:
            # This is so that the user can force updates of the display of a note.
            proxy_index = self.indexAt(event.pos())
            if (len(self.selectedIndexes()) > 0) and (proxy_index == self.selectedIndexes()[0]):
                self.selectedNoteChanged.emit(self.noteFromProxyIndex(proxy_index))
            else:
                QtGui.QListView.mousePressEvent(self, event)


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
        self.attachments = []
        self.cur_version_number = 0
        self.date = None
        self.keywords = []
        self.markdown = None
        self.name = ""
        self.notebook = notebook
        self.unsaved_markdown = None
        self.versions = []
        
        # Load an old note.
        if note_file is not None:
            self.fullname = note_file
            self.filename = os.path.basename(self.fullname)

            # These are the git SHA-1 keys of the versions. The array
            # is ordered with the most recent version last.
            self.versions = self.notebook.getNoteVersions(self.filename)

            self.cur_version_number = len(self.versions)-1
            self.loadNote(self.cur_version_number)
            
        # Create a new note.
        else:
            self.markdown = ""
            self.name = note_name
            self.filename = "note_" + str(uuid.uuid1()) + ".xml"
            self.fullname = self.notebook.getDirectory() + self.filename
            
        QtGui.QStandardItem.__init__(self, self.name + " (" + str(len(self.versions)) +")")

    def addAttachment(self, attachment_fullname):
        self.attachments.append(attachment_fullname)
        
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

    def getAttachments(self):
        return self.attachments
        
    def getCurrentVersionNumber(self):
        return self.cur_version_number

    def getFileName(self):
        return self.filename

    def getLink(self):
        """
        This returns a link to the current latest version of the note
        """
        return self.filename + "&v=" + str(self.getNumberOfVersions() - 1)
        
    def getMarkdown(self):
        return self.markdown
    
    def getName(self):
        return self.name

    def getNotebook(self):
        return self.notebook

    def getNumberOfVersions(self):
        return len(self.versions)
        
    def getUnsavedMarkdown(self):
        return self.unsaved_markdown

    def isLatestVersion(self):
        return (self.cur_version_number == (self.getNumberOfVersions() - 1))
        
    def loadNote(self, version_index):
        self.cur_version_number = version_index
        xml_text = misc.gitGetVersion(self.notebook.getDirectory(),
                                      self.filename,
                                      self.versions[version_index])
        xml = ElementTree.fromstring(xml_text)
        self.date = xml.find("date").text
        self.markdown = xml.find("markdown").text
        self.name = xml.find("name").text

        attach_xml = xml.find("attachments")
        if attach_xml is not None:
            for xml in attach_xml:
                self.attachments.append(xml.text)

    def moveNote(self, new_notebook):
        """
        Notebooks are just directories, so update the filename accordingly.

        new_notebook is a NotebookStandardItem.
        """
        self.notebook = new_notebook
        self.filename = self.notebook.getDirectory() + self.uuid

        # FIXME: Need to replay and commit the versions so that the history
        #        is not lost when switching notebooks.
        #        We also need to move the attachments.

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

        date_xml = ElementTree.SubElement(xml, "date")
        date_xml.text = str(datetime.datetime.now())
        
        markdown_xml = ElementTree.SubElement(xml, "markdown")
        markdown_xml.text = self.markdown

        if (len(self.attachments) > 0):
            attachments_xml = ElementTree.SubElement(xml, "attachments")
            for attached in self.attachments:
                file_xml = ElementTree.SubElement(attachments_xml, "file")
                file_xml.text = attached

        if (len(self.keywords) > 0):
            keywords_xml = ElementTree.SubElement(xml, "keywords")
            for word in self.keywords:
                word_xml = ElementTree.SubElement(keywords_xml, "word")
                word_xml.text = word

        misc.pSaveXML(self.fullname, xml)

        # Delete backup.
        
        # git commit.
        misc.gitSave(self.notebook.getDirectory(),
                     self.filename,
                     "update " + self.name)

        # append current version to the list of versions.
        self.versions.append(misc.gitGetLastCommitId(self.notebook.getDirectory()))
        self.cur_version_number = len(self.versions)-1

        self.setText(self.name + " (" + str(len(self.versions)) +")")
        
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

    
