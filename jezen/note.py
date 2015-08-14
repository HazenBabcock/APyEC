#!/usr/bin/env python
"""
.. module:: note
   :synopsis: The Note class.
"""

import datetime
import glob
import markdown
import os
import uuid
import shutil

from PyQt4 import QtCore, QtGui

from xml.etree import ElementTree

import logger
import misc


class NoteContent(object):
    """
    The content, keywords, attachments, etc.. of a single version of a single note.
    There can be many of these associated with a single NoteStandardItem.
    """
    @logger.logFn
    def __init__(self, note, version_number, xml = None):
        """
        Creates a blank note and fills in the fields from the xml if it is provided.
        """
        self.attachments = []
        self.content = ""
        self.content_type = "markdown"
        self.date = None
        self.html_converter = markdown.markdown
        self.keywords = []
        self.name = note.getName()
        self.note = note
        self.unsaved_content = None
        self.version_number = version_number

        if xml is not None:
            self.date = xml.find("date").text
            self.content = xml.find("content").text
            self.content_type = xml.find("content_type").text
            self.name = xml.find("name").text

            attach_xml = xml.find("attachments")
            if attach_xml is not None:
                for xml in attach_xml:
                    self.attachments.append(xml.text)

            keyword_xml = xml.find("keywords")
            if keyword_xml is not None:
                for xml in keyword_xml:
                    self.keywords.append(xml.text)

    @logger.logFn        
    def addAttachment(self, attachment_fullname):
        self.attachments.append(attachment_fullname)
                    
    @logger.logFn
    def contentToXML(self, xml, use_current_time):
        """
        Add the note contents to the xml.
        """
        name_xml = ElementTree.SubElement(xml, "name")
        name_xml.text = self.name

        date_xml = ElementTree.SubElement(xml, "date")
        if use_current_time:
            date_xml.text = str(datetime.datetime.now())
        else:
            date_xml.text = self.date
        
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

        content_xml = ElementTree.SubElement(xml, "content")
        content_xml.text = self.content

        content_type_xml = ElementTree.SubElement(xml, "content_type")
        content_type_xml.text = self.content_type

        # Delete backup..

    @logger.logFn    
    def convertToHTML(self, content):
        return self.html_converter(content)

    @logger.logFn    
    def getAttachments(self):
        return self.attachments

    @logger.logFn    
    def getContent(self):
        return self.content

    @logger.logFn    
    def getContentType(self):
        return self.content_type

    @logger.logFn
    def getDate(self):
        return datetime.datetime.strptime(self.date, '%Y-%m-%d %H:%M:%S.%f')
    
    @logger.logFn
    def getKeywords(self):
        return self.keywords

    @logger.logFn    
    def getName(self):
        return self.name
    
    @logger.logFn
    def getNoteStandardItem(self):
        return self.note

    @logger.logFn    
    def getUnsavedContent(self):
        return self.unsaved_content
    
    @logger.logFn    
    def getVersionNumber(self):
        return self.version_number    

    @logger.logFn
    def removeAttachment(self, attachment_fullname):
        self.attachments.remove(attachment_fullname)
        
    @logger.logFn        
    def saveBackup(self):
        backup_name = self.note.getFullname()[:-4] + "_backup.txt"
        with open(backup_name, "w") as fp:
            fp.write(self.content)

    @logger.logFn        
    def setContent(self, new_content):
        self.content = new_content

    @logger.logFn
    def setKeywords(self, new_keywords):
        self.keywords = new_keywords

    @logger.logFn
    def setName(self, new_name):
        self.name = new_name
        
    @logger.logFn        
    def setUnsavedContent(self, new_content):
        self.unsaved_content = new_content
        

class NoteMVC(QtGui.QListView):
    """
    Encapsulates a list view specialized for notes and it's associated model.
    """
    addNewNote = QtCore.pyqtSignal()
    copyNote = QtCore.pyqtSignal(object)
    editNote = QtCore.pyqtSignal(object, object)
    moveNote = QtCore.pyqtSignal(object)
    noteKeywordsChanged = QtCore.pyqtSignal(list, list)
    selectedNoteChanged = QtCore.pyqtSignal(object)

    @logger.logFn    
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
        self.editNoteAction = QtGui.QAction(self.tr("Edit Note"), self)
        self.editNoteAction.triggered.connect(self.handleEditNote)
        self.moveNoteAction = QtGui.QAction(self.tr("Move Note"), self)
        self.moveNoteAction.triggered.connect(self.handleMoveNote)
        self.newNoteAction = QtGui.QAction(self.tr("New Note"), self)
        self.newNoteAction.triggered.connect(self.handleNewNote)
        self.renameNoteAction = QtGui.QAction(self.tr("Rename Note"), self)
        self.renameNoteAction.triggered.connect(self.handleRenameNote)

        self.note_popup_menu = QtGui.QMenu(self)
        self.note_popup_menu.addAction(self.copyLinkAction)
        self.note_popup_menu.addAction(self.copyNoteAction)
        self.note_popup_menu.addAction(self.deleteNoteAction)
        self.note_popup_menu.addAction(self.editNoteAction)
        self.note_popup_menu.addAction(self.moveNoteAction)
        self.note_popup_menu.addAction(self.newNoteAction)
        self.note_popup_menu.addAction(self.renameNoteAction)        

        self.no_note_popup_menu = QtGui.QMenu(self)
        self.no_note_popup_menu.addAction(self.newNoteAction)

        # Note model
        self.note_model = NoteStandardItemModel(self)
        self.note_proxy_model = NoteSortFilterProxyModel(self)
        self.note_proxy_model.setSourceModel(self.note_model)
        self.setModel(self.note_proxy_model)

        # Get selection changes.
        self.selectionModel().selectionChanged.connect(self.handleSelectionChange)

    @logger.logFn        
    def addNote(self, notebook, name):
        """
        Add a new blank note.
        """
        a_note = NoteStandardItem(notebook, self.noteKeywordsChanged, note_name = name)
        self.notes[a_note.getFileName()] = a_note
        self.note_model.appendRow(a_note)
        self.note_proxy_model.sort(0)

    @logger.logFn        
    def clearNotes(self):
        self.note_model.clear()

    @logger.logFn
    def copyANote(self, notebook, old_note):
        # FIXME: Should save note history?
        new_note = NoteStandardItem(notebook,
                                    self.noteKeywordsChanged,
                                    note_name = old_note.getName() + " copy")
        self.notes[new_note.getFileName()] = new_note
        new_note.saveNote(old_note.loadNoteContent(old_note.getLatestVersionNumber()))
        self.note_model.appendRow(new_note)
        self.note_proxy_model.sort(0)
        
    @logger.logFn
    def handleCopyLink(self, boolean):
        clipboard = QtGui.QApplication.clipboard()
        a_note = self.noteFromProxyIndex(self.right_clicked)

        # FIXME: This should depend on note content type.
        clipboard.setText("[" + a_note.getName() + "](" + a_note.getLink() + ")")

    @logger.logFn
    def handleCopyNote(self, boolean):
        self.copyNote.emit(self.noteFromProxyIndex(self.right_clicked))

    @logger.logFn
    def handleDeleteNote(self, boolean):
        a_note = self.noteFromProxyIndex(self.right_clicked)
        a_note_name = a_note.getName()

        reply = QtGui.QMessageBox.question(self,
                                           "Warning!",
                                           "Really delete note '" + a_note_name + "'?",
                                           QtGui.QMessageBox.Yes,
                                           QtGui.QMessageBox.No)
        if (reply == QtGui.QMessageBox.Yes):
            source_index = self.note_proxy_model.mapToSource(self.right_clicked)
            self.note_model.removeRow(source_index.row())
            del self.notes[a_note.getFileName()]            
            a_note.deleteNote()

            if (len(self.selectedIndexes()) == 0):
                self.selectedNoteChanged.emit(None)

    @logger.logFn
    def handleEditNote(self, boolean):
        a_note = self.noteFromProxyIndex(self.right_clicked)
        note_content = a_note.loadNoteContent(a_note.getLatestVersionNumber())
        self.editNote.emit(a_note, note_content)
        
    @logger.logFn
    def handleNewNote(self, boolean):
        self.addNewNote.emit()

    @logger.logFn
    def handleMoveNote(self, boolean):
        self.moveNote.emit(self.noteFromProxyIndex(self.right_clicked))
    
    @logger.logFn    
    def handleNoteLinkClicked(self, note_filename, note_version):
        note_filename = str(note_filename)
        if note_filename in self.notes:
            a_note = self.notes[note_filename]
            source_index = self.note_model.indexFromItem(a_note)
            filter_index = self.note_proxy_model.mapFromSource(source_index)
            if filter_index.isValid():
                self.setCurrentIndex(filter_index)
            else:
                self.clearSelection()
                self.selectedNoteChanged.emit(a_note)

    @logger.logFn
    def handleRenameNote(self, boolean):
        a_note = self.noteFromProxyIndex(self.right_clicked)
        a_note_name = a_note.getName()
        [new_name, ok] = QtGui.QInputDialog.getText(self,
                                                    'Rename Note',
                                                    'Enter a new name:',
                                                    text = a_note_name)
        if ok:
            a_note.rename(new_name)
            self.note_proxy_model.sort(0)

    @logger.logFn                
    def handleSelectionChange(self, new_item_selection, old_item_selection):
        if (len(self.selectedIndexes()) > 0):
            self.selectedNoteChanged.emit(self.noteFromProxyIndex(self.selectedIndexes()[0]))

    @logger.logFn
    def handleSortBy(self, sort_mode):
        """
        Sort by (0) name, (1) date created, (2) date modified.
        """
        self.note_proxy_model.setSortMode(sort_mode)
        self.note_proxy_model.sort(0)
        
    @logger.logFn            
    def loadNotes(self, notebook):
        """
        Loads all the notes in a notebook.
        """
        note_files = glob.glob(notebook.getDirectory() + "note_*.xml")
        for n_file in note_files:
            a_note = NoteStandardItem(notebook, self.noteKeywordsChanged, note_file = n_file)
            self.notes[a_note.getFileName()] = a_note
            self.note_model.appendRow(a_note)

        notebook.setNumberNotes(len(note_files))
        self.note_proxy_model.sort(0)

    @logger.logFn        
    def mousePressEvent(self, event):
        if (event.button() == QtCore.Qt.RightButton):
            self.right_clicked = self.indexAt(event.pos())
            if (self.right_clicked.row() > -1):
                self.note_popup_menu.exec_(event.globalPos())
            else:
                self.no_note_popup_menu.exec_(event.globalPos())
        else:
            # This is so that the user can force updates of the display of a note.
            proxy_index = self.indexAt(event.pos())
            if (len(self.selectedIndexes()) > 0) and (proxy_index == self.selectedIndexes()[0]):
                self.selectedNoteChanged.emit(self.noteFromProxyIndex(proxy_index))
            else:
                QtGui.QListView.mousePressEvent(self, event)

    @logger.logFn
    def moveANote(self, notebook, a_note):
        a_note.moveNote(notebook)
        self.note_proxy_model.invalidateFilter()

    @logger.logFn        
    def noteFromProxyIndex(self, proxy_index):
        source_index = self.note_proxy_model.mapToSource(proxy_index)
        return self.note_model.itemFromIndex(source_index)                

    @logger.logFn    
    def updateKeywordFilter(self, keywords):
        self.note_proxy_model.setKeywords(keywords)
        self.note_proxy_model.sort(0)

    @logger.logFn    
    def updateNotebookFilter(self, notebooks):
        self.note_proxy_model.setNotebooks(notebooks)
        self.note_proxy_model.sort(0)        
                


class NoteSortFilterProxyModel(QtGui.QSortFilterProxyModel):
    """
    Sort and filter notes. At the start (or when changing directories) we
    load all the notes, but only show the ones that match the filters.
    """
    @logger.logFn    
    def __init__(self, parent = None):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        self.keywords = []
        self.notebooks = []
        self.sort_mode = "Name"

    @logger.logFn        
    def filterAcceptsRow(self, source_row, source_parent):
        index = self.sourceModel().index(source_row, 0, source_parent)
        note = self.sourceModel().itemFromIndex(index)
        accept = False

        # Check notebooks.
        if (note.getNotebook() in self.notebooks):
            accept = True

        # Check keywords. An empty keyword list is equivalent to no selection.
        if accept:
            if (len(self.keywords) > 0):
                accept = any(x in self.keywords for x in note.getKeywords())

        return accept

    def lessThan(self, left, right):
        """
        Custom sorting.
        """
        if (self.sort_mode == "Name"):
            # Use default sorting to sort by note name.
            return QtGui.QSortFilterProxyModel.lessThan(self, left, right)
        else:
            left_note = self.sourceModel().itemFromIndex(left)
            right_note = self.sourceModel().itemFromIndex(right)            
            if (self.sort_mode == "Date Created"):
                return (left_note.date_created < right_note.date_created)
            else:
                return (left_note.date_modified < right_note.date_modified)
        
    @logger.logFn    
    def setKeywords(self, new_keywords):
        self.keywords = new_keywords
        self.invalidateFilter()
        
    @logger.logFn    
    def setNotebooks(self, new_notebooks):
        self.notebooks = new_notebooks
        self.invalidateFilter()

    @logger.logFn
    def setSortMode(self, sort_mode):
        self.sort_mode = sort_mode
        
    
class NoteStandardItem(QtGui.QStandardItem):
    """
    A single note.
    This class also handles loading and saving the notes contents. There
    is only one of these per note.
    """
    @logger.logFn
    def __init__(self, notebook, keywords_changed_signal, note_file = None, note_name = None):
        """
        Load on old note (when given a note_file), or create a
        new note (when given a name).

        notebook is a NotebookStandardItem.

        note_file is path/note_(uuid).xml
        """
        self.date_created = None
        self.date_modified = None
        self.filname = ""
        self.fullname = ""
        self.keywords = []
        self.keywords_changed_signal = keywords_changed_signal
        self.name = ""
        self.notebook = notebook
        self.old_keywords = []
        self.versions = []
        
        # Load an old note.
        if note_file is not None:
            self.fullname = note_file
            self.filename = os.path.basename(self.fullname)

            # These are the git SHA-1 keys of the versions. The array
            # is ordered with the most recent version last.
            self.versions = self.notebook.getNoteVersions(self.filename)

            note_content = self.loadNoteContent(0)
            self.date_created = note_content.getDate()
            
            note_content = self.loadNoteContent(len(self.versions) - 1)
            self.date_modified = note_content.getDate()
            self.name = note_content.getName()

            if 0:
                print self.name
                print str(self.date_created)
                print str(self.date_modified)
                print ""
                
            # For now, keywords are always from the most recently saved
            # version of the note. This may need improvement down the road?
            self.keywords = list(note_content.getKeywords())
            
        # Create a new note.
        else:
            self.date_created = datetime.datetime.now()
            self.date_modified = datetime.datetime.now()
            self.name = note_name
            self.filename = "note_" + str(uuid.uuid1()) + ".xml"
            self.fullname = self.notebook.getDirectory() + self.filename
            
        QtGui.QStandardItem.__init__(self, self.name + " (" + str(len(self.versions)) +")")

    @logger.logFn
    def checkKeywords(self, note_content):
        new_keywords = list(note_content.getKeywords())
        if (set(self.old_keywords) != set(new_keywords)):
            self.keywords_changed_signal.emit(self.old_keywords, new_keywords)
            self.old_keywords = new_keywords
            
    @logger.logFn    
    def deleteNote(self):
        """
        Remove the note file from the disk and create a git commit.
        """
        # FIXME: Maybe notes should just be marked as deleted, but still
        #  exist so that any old links to them would still work?
        misc.gitRemove(self.notebook.getDirectory(),
                       self.filename,
                       "remove " + self.name)

    @logger.logFn    
    def getFileName(self):
        return self.filename

    @logger.logFn    
    def getFullName(self):
        return self.fullname

    @logger.logFn
    def getKeywords (self):
        return self.keywords

    @logger.logFn
    def getLatestVersionNumber(self):
        return self.getNumberOfVersions() - 1
    
    @logger.logFn    
    def getLink(self):
        """
        This returns a link to the most recent version of the note
        """
        return self.filename + "&v=" + str(self.getLatestVersionNumber())

    @logger.logFn
    def getName(self):
        return self.name
    
    @logger.logFn    
    def getNotebook(self):
        return self.notebook

    @logger.logFn    
    def getNumberOfVersions(self):
        return len(self.versions)

    @logger.logFn    
    def isLatestVersion(self, note_content):
        return (note_content.getVersionNumber() == self.getLatestVersionNumber())

    @logger.logFn
    def loadNoteContent(self, version_number):
        """
        Load a version and return it as a NoteContent object.
        """
        
        # Handle newly created notes.
        if (self.getNumberOfVersions() == 0):
            return NoteContent(self, -1)

        # Load the XML of an existing note.
        xml_text = misc.gitGetVersion(self.notebook.getDirectory(),
                                      self.filename,
                                      self.versions[version_number])
        xml = ElementTree.fromstring(xml_text)

        note_content = NoteContent(self, version_number, xml)

        # Check if the keywords have changed.
        self.checkKeywords(note_content)

        return note_content

    @logger.logFn                
    def moveNote(self, new_notebook):
        """
        Notebooks are just directories, so update the filename accordingly.

        new_notebook is a NotebookStandardItem.
        """

        # Load all versions of the note in the old notebook
        # and all of the (unique) attachments.
        attachments = {}
        note_contents = []
        for v_number in range(self.getNumberOfVersions()):
            note_content = self.loadNoteContent(v_number)
            note_contents.append(note_content)
            for fullname in note_content.getAttachments():
                attachments[fullname] = True

        # Move attachments.
        old_dir = self.notebook.getDirectory()
        new_dir = new_notebook.getDirectory()
        for fullname in attachments.keys():
            filename = os.path.basename(fullname)
            os.makedirs(new_dir + os.path.dirname(fullname))
            shutil.copy(old_dir + fullname, new_dir + fullname)
            misc.gitRemove(old_dir,
                           fullname,
                           "remove attachment " + filename)
            misc.gitAddCommit(new_dir,
                              fullname,
                              "attachment " + filename)

        # Delete old note.
        self.deleteNote()
        
        # Move to new notebook.
        # FIXME: If this gets move to a new notebook, then back to the old
        #  notebook it will appear as completely new note. However if we
        #  don't do this then the version history of the note will get all
        #  messed up.
        self.notebook = new_notebook
        self.filename = "note_" + str(uuid.uuid1()) + ".xml"
        self.fullname = self.notebook.getDirectory() + self.filename
        self.versions = []
            
        # Replay history in the new notebook.
        for content in note_contents:
            self.saveNote(content, use_current_time = False)

    @logger.logFn
    def rename(self, new_name):
        self.name = str(new_name)
        self.setText(new_name)

        # Load latest note content and save with new name creating a git commit.
        note_content = self.loadNoteContent(self.getLatestVersionNumber())
        note_content.setName(self.name)
        self.saveNote(note_content)

    @logger.logFn            
    def saveNote(self, note_content, use_current_time = True):
        """
        Save XML and create a git commit.
        """

        # Save XML.
        xml = ElementTree.Element("note")
        note_content.contentToXML(xml, use_current_time)
        misc.pSaveXML(self.fullname, xml)
        
        # git commit.
        misc.gitAddCommit(self.notebook.getDirectory(),
                          self.filename,
                          "update " + self.name)

        # Append current version to the list of versions.
        self.versions.append(misc.gitGetLastCommitId(self.notebook.getDirectory()))
        self.setText(self.name + " (" + str(len(self.versions)) +")")

        # Check if the keywords have changed.
        self.checkKeywords(note_content)

        # For now, keywords are always from the most recently saved
        # version of the note. This may need improvement down the road?
        self.keywords = list(note_content.getKeywords())

        
class NoteStandardItemModel(QtGui.QStandardItemModel):
    """
    The note listview model.
    """
    @logger.logFn    
    def __init__(self, parent = None):
        QtGui.QStandardItemModel.__init__(self, parent)

    
