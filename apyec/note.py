#!/usr/bin/env python
"""
.. module:: note
   :synopsis: The Note class.
"""

import datetime
import glob
import os
import uuid
import shutil

from PyQt5 import QtCore, QtGui, QtWidgets

from xml.etree import ElementTree

import converters
import logger
import misc


class NoteContent(object):
    """
    The content, keywords, attachments, etc.. of a single version of a single note.
    There can be many of these associated with a single NoteStandardItem.
    """
    @logger.logFn
    def __init__(self, note, version, xml = None, **kwds):
        """
        Creates a blank note and fills in the fields from the xml if it is provided.
        """
        super().__init__(**kwds)
        
        self.attachments = []
        self.content = ""
        self.content_type = "markdown"
        self.date = None
        self.html_converter = None
        self.keywords = []
        self.link_converter = None
        self.name = note.getName()
        self.note = note
        self.unsaved_content = None
        self.version = version

        if xml is not None:
            self.date = xml.find("date").text
            self.content = xml.find("content").text
            if self.content is None:
                self.content = ""
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

        self.setConverters(self.content_type)

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
    def formatLink(self, link_name, link_url, is_image = False):
        return self.link_converter(link_name, link_url, is_image)
    
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
        if self.date is not None:
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
    def getVersion(self):
        return self.version

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
    def setContentType(self, content_type):
        self.content_type = str(content_type)
        self.setConverters(self.content_type)
        
    @logger.logFn
    def setConverters(self, content_type):
        self.html_converter = converters.getHTMLConverter(content_type)
        self.link_converter = converters.getLinkConverter(content_type)
                         
    @logger.logFn
    def setKeywords(self, new_keywords):
        self.keywords = new_keywords

    @logger.logFn
    def setName(self, new_name):
        self.name = new_name
        
    @logger.logFn        
    def setUnsavedContent(self, new_content):
        self.unsaved_content = new_content
        

class NoteListViewDelegate(QtWidgets.QStyledItemDelegate):
    """
    A custom look for each note item.
    """
    def __init__(self, model, proxy_model, **kwds):
        super().__init__(**kwds)

        self.model = model
        self.proxy_model = proxy_model

    def itemFromProxyIndex(self, proxy_index):
        source_index = self.proxy_model.mapToSource(proxy_index)
        return self.model.itemFromIndex(source_index)
    
    def paint(self, painter, option, index):
        note = self.itemFromProxyIndex(index)

        # Draw correct background.
        style = option.widget.style()
        style.drawControl(QtWidgets.QStyle.CE_ItemViewItem, option, painter, option.widget)

        # Draw text.
        upper_rect = QtCore.QRect(option.rect.left(),
                                  option.rect.top(),
                                  option.rect.width(),
                                  option.rect.height() * 0.45)
        
        lower_rect = QtCore.QRect(option.rect.left(),
                                  option.rect.top() + option.rect.height() * 0.45,
                                  option.rect.width(),
                                  option.rect.height() * 0.9)
        
        painter.drawText(upper_rect, QtCore.Qt.AlignLeft, " " + note.getName())
        painter.drawText(upper_rect, QtCore.Qt.AlignRight, "(" + str(note.getNumberOfVersions()) + " versions) ")
        painter.drawText(lower_rect,
                         QtCore.Qt.AlignLeft,
                         " created on " + datetime.datetime.strftime(note.date_created, '%Y-%m-%d'))

    def sizeHint(self, option, index):
        result = QtWidgets.QStyledItemDelegate.sizeHint(self, option, index)
        result.setHeight(2.2 * result.height())
        return result
        
    
class NoteMVC(QtWidgets.QListView):
    """
    Encapsulates a list view specialized for notes and it's associated model.
    """
    addNewNote = QtCore.pyqtSignal()
    copyNote = QtCore.pyqtSignal(object)
    editNote = QtCore.pyqtSignal(object, object)
    moveNote = QtCore.pyqtSignal(object)
    noteKeywordsChanged = QtCore.pyqtSignal(list, list)
    selectedNoteChanged = QtCore.pyqtSignal(object, object)

    @logger.logFn    
    def __init__(self, parent = None):
        super().__init__(parent)

        self.notes = {}
        self.note_version = None
        self.right_clicked = None

        # Context menu
        self.copyLinkAction = QtWidgets.QAction(self.tr("Copy Link to Clipboard"), self)
        self.copyLinkAction.triggered.connect(self.handleCopyLink)
        self.copyNoteAction = QtWidgets.QAction(self.tr("Copy Note"), self)
        self.copyNoteAction.triggered.connect(self.handleCopyNote)
        self.deleteNoteAction = QtWidgets.QAction(self.tr("Delete Note"), self)
        self.deleteNoteAction.triggered.connect(self.handleDeleteNote)
        self.editNoteAction = QtWidgets.QAction(self.tr("Edit Note"), self)
        self.editNoteAction.triggered.connect(self.handleEditNote)
        self.moveNoteAction = QtWidgets.QAction(self.tr("Move Note"), self)
        self.moveNoteAction.triggered.connect(self.handleMoveNote)
        self.newNoteAction = QtWidgets.QAction(self.tr("New Note"), self)
        self.newNoteAction.triggered.connect(self.handleNewNote)
        self.renameNoteAction = QtWidgets.QAction(self.tr("Rename Note"), self)
        self.renameNoteAction.triggered.connect(self.handleRenameNote)

        self.note_popup_menu = QtWidgets.QMenu(self)
        self.note_popup_menu.addAction(self.copyLinkAction)
        self.note_popup_menu.addAction(self.copyNoteAction)
        self.note_popup_menu.addAction(self.deleteNoteAction)
        self.note_popup_menu.addAction(self.editNoteAction)
        self.note_popup_menu.addAction(self.moveNoteAction)
        self.note_popup_menu.addAction(self.newNoteAction)
        self.note_popup_menu.addAction(self.renameNoteAction)        

        self.no_note_popup_menu = QtWidgets.QMenu(self)
        self.no_note_popup_menu.addAction(self.newNoteAction)

        # Note model
        self.note_model = NoteStandardItemModel(parent = self)
        self.note_proxy_model = NoteSortFilterProxyModel(parent = self)
        self.note_proxy_model.setSourceModel(self.note_model)
        self.setModel(self.note_proxy_model)

        # Rendering
        self.setItemDelegate(NoteListViewDelegate(self.note_model, self.note_proxy_model))
        
        # Get selection changes.
        self.selectionModel().selectionChanged.connect(self.handleSelectionChange)

    @logger.logFn        
    def addNote(self, notebook, name):
        """
        Add a new blank note.
        """
        a_note = NoteStandardItem(notebook, self.noteKeywordsChanged, note_name = name)
        a_note.getNotebook().incNumberNotes(1)
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
        new_note.saveNote(old_note.loadNoteContent(old_note.getLatestVersion()))
        new_note.getNotebook().incNumberNotes(1)
        self.note_model.appendRow(new_note)
        self.note_proxy_model.sort(0)
        
    @logger.logFn
    def handleCopyLink(self, boolean):
        """
        This returns the filename and location which can be used to create a hyperlink.
        """
        clipboard = QtWidgets.QApplication.clipboard()
        a_note = self.noteFromProxyIndex(self.right_clicked)
        clipboard.setText("<note_link><split>" + a_note.getName() + "<split>" + a_note.getLink() + "<split></note_link>")

    @logger.logFn
    def handleCopyNote(self, boolean):
        self.copyNote.emit(self.noteFromProxyIndex(self.right_clicked))

    @logger.logFn
    def handleDeleteNote(self, boolean):
        a_note = self.noteFromProxyIndex(self.right_clicked)
        a_note_name = a_note.getName()

        reply = QtWidgets.QMessageBox.question(self,
                                               "Warning!",
                                               "Really delete note '" + a_note_name + "'?",
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if (reply == QtWidgets.QMessageBox.Yes):
            source_index = self.note_proxy_model.mapToSource(self.right_clicked)
            self.note_model.removeRow(source_index.row())
            del self.notes[a_note.getFileName()]            
            a_note.deleteNote()
            a_note.getNotebook().incNumberNotes(-1)

            if (len(self.selectedIndexes()) == 0):
                self.selectedNoteChanged.emit(None, None)

    @logger.logFn
    def handleEditNote(self, boolean):
        a_note = self.noteFromProxyIndex(self.right_clicked)
        note_content = a_note.loadNoteContent(a_note.getLatestVersion())
        self.editNote.emit(a_note, note_content)

    @logger.logFn
    def handleMoveNote(self, boolean):
        self.moveNote.emit(self.noteFromProxyIndex(self.right_clicked))
        
    @logger.logFn
    def handleNewNote(self, boolean):
        self.addNewNote.emit()
    
    @logger.logFn
    def handleNoteLinkClicked(self, note_filename, note_version):
        note_filename = str(note_filename)
        if note_filename in self.notes:
            a_note = self.notes[note_filename]
            source_index = self.note_model.indexFromItem(a_note)
            filter_index = self.note_proxy_model.mapFromSource(source_index)
            if filter_index.isValid():
                # Temporarily record this so that the right version will get loaded.
                self.note_version = note_version
                self.setCurrentIndex(filter_index)
            else:
                self.clearSelection()
                self.selectedNoteChanged.emit(a_note, note_version)
        
    @logger.logFn
    def handleRenameNote(self, boolean):
        a_note = self.noteFromProxyIndex(self.right_clicked)
        a_note_name = a_note.getName()
        [new_name, ok] = QtWidgets.QInputDialog.getText(self,
                                                        'Rename Note',
                                                        'Enter a new name:',
                                                        text = a_note_name)
        if ok:
            a_note.rename(new_name)
            self.note_proxy_model.sort(0)

    @logger.logFn                
    def handleSelectionChange(self, new_item_selection, old_item_selection):
        if (len(self.selectedIndexes()) > 0):
            self.selectedNoteChanged.emit(self.noteFromProxyIndex(self.selectedIndexes()[0]), self.note_version)
            self.note_version = None

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
                self.selectedNoteChanged.emit(self.noteFromProxyIndex(proxy_index), None)
            else:
                super().mousePressEvent(event)

    @logger.logFn
    def moveANote(self, notebook, a_note):
        a_note.getNotebook().incNumberNotes(-1)
        a_note.moveNote(notebook)
        a_note.getNotebook().incNumberNotes(1)        
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
        
    @logger.logFn
    def updateNoteDisplay(self, note):
        if (len(self.selectedIndexes()) > 0):
            cur_note = self.noteFromProxyIndex(self.selectedIndexes()[0])
            if (note == cur_note):
                self.selectedNoteChanged.emit(cur_note, None)


class NoteSortFilterProxyModel(QtCore.QSortFilterProxyModel):
    """
    Sort and filter notes. At the start (or when changing directories) we
    load all the notes, but only show the ones that match the filters.
    """
    @logger.logFn    
    def __init__(self, **kwds):
        super().__init__(**kwds)

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
        left_note = self.sourceModel().itemFromIndex(left)
        right_note = self.sourceModel().itemFromIndex(right)
        if (self.sort_mode == "Name"):

            # If the names are the same, sort by date.
            if (left_note.name == right_note.name):
                return (left_note.date_created < right_note.date_created)

            # Otherwise sort by name.
            else:
                return (left_note.name < right_note.name)

        else:
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

    This class also handles loading and saving the notes contents.

    This class also tracks the current note editor so that there is
    never more than one open at a time.
    """
    @logger.logFn
    def __init__(self, notebook, keywords_changed_signal, note_file = None, note_name = None, **kwds):
        """
        Load on old note (when given a note_file), or create a
        new note (when given a name).

        notebook is a NotebookStandardItem.

        note_file is path/note_(uuid).xml
        """
        super().__init__(**kwds)
        
        self.date_created = None
        self.date_modified = None
        self.editor = None
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

            note_content = self.loadNoteContent(self.versions[0])
            self.date_created = note_content.getDate()
            
            note_content = self.loadNoteContent(self.versions[-1])
            self.date_modified = note_content.getDate()
            self.name = note_content.getName()

            if False:
                print(self.name)
                print(str(self.date_created))
                print(str(self.date_modified))
                print("")
                
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
        self.setEditable(False)
        self.setToolTip(self.filename)

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
        self.notebook.setUnpushed()

    @logger.logFn
    def getEditor(self):
        return self.editor
    
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
    def getLatestVersion(self):
        if (len(self.versions) > 0):
            return self.versions[-1]
        else:
            return "empty"
    
    @logger.logFn    
    def getLink(self, version = None):
        """
        This returns a link to a version of a note (if specified), otherwise 
        it returns a link to the most recent version of the note.
        """
        if version is None:
            return self.filename + "&v=" + self.getLatestVersion()
        else:
            return self.filename + "&v=" + version
        
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
    def getVersions(self):
        return self.versions
        
    @logger.logFn    
    def isLatestVersion(self, note_content):
        return (note_content.getVersion() == self.getLatestVersion())

    @logger.logFn
    def loadNoteContent(self, version):
        """
        Load a version and return it as a NoteContent object.
        """
        
        # Handle newly created notes.
        if (len(self.versions) == 0):
            return NoteContent(self, "empty")

        # Load the XML of an existing note.
        xml_text = misc.gitGetVersion(self.notebook.getDirectory(),
                                      self.filename,
                                      version)
        xml = ElementTree.fromstring(xml_text)

        note_content = NoteContent(self, version, xml)

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
        for version in self.versions:
            note_content = self.loadNoteContent(version)
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
            
        self.notebook.setUnpushed()            

    @logger.logFn
    def rename(self, new_name):
        self.name = str(new_name)
        self.setText(new_name)

        # Load latest note content and save with new name creating a git commit.
        note_content = self.loadNoteContent(self.getLatestVersion())
        note_content.setName(self.name)
        self.saveNote(note_content)
        
        self.notebook.setUnpushed()

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

        self.notebook.setUnpushed()
        
    @logger.logFn
    def setEditor(self, editor):
        self.editor = editor
        
        
class NoteStandardItemModel(QtGui.QStandardItemModel):
    """
    The note listview model.
    """
    @logger.logFn    
    def __init__(self, **kwds):
        super().__init__(**kwds)


    
