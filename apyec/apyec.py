#!/usr/bin/env python

import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

import apyec_ui as apyecUi

import editor
import logger
import misc
import notebook


class APyEC(QtWidgets.QMainWindow):

    def __init__(self, **kwds):
        super().__init__(**kwds)

        self.email = ""
        self.settings = QtCore.QSettings("apyec", "apyec")
        self.username = ""

        logger.startLogging("./logs/")
            
        # Load UI
        self.ui = apyecUi.Ui_MainWindow()
        self.ui.setupUi(self)

        self.viewer = editor.Viewer(parent = self.ui.noteGroupBox)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.viewer)
        self.ui.noteGroupBox.setLayout(layout)

        self.ui.sortbyComboBox.addItem("Name")
        self.ui.sortbyComboBox.addItem("Date Created")
        self.ui.sortbyComboBox.addItem("Date Modified")
            
        # Load settings
        self.directory = str(self.settings.value("directory", "./"))

        # Restore geometry
        self.move(self.settings.value("main_window.pos", QtCore.QPoint(100,100)))
        self.resize(self.settings.value("main_window.size", self.size()))
        self.ui.mainSplitter.restoreState(self.settings.value("main_splitter", self.ui.mainSplitter.saveState()))
        self.ui.notebookSplitter.restoreState(self.settings.value("notebook_splitter", self.ui.notebookSplitter.saveState()))

        # Connect signals
        self.ui.actionNew_Note.triggered.connect(self.handleNewNote)
        self.ui.actionNew_Notebook.triggered.connect(self.handleNewNotebook)
        self.ui.actionPrint_Note.triggered.connect(self.viewer.handlePrint)
        self.ui.actionSet_Directory.triggered.connect(self.handleSetDirectory)
        self.ui.actionQuit.triggered.connect(self.handleQuit)
        self.ui.sortbyComboBox.currentIndexChanged[str].connect(self.ui.noteMVC.handleSortBy)

        self.ui.keywordChooserMVC.selectedKeywordsChanged.connect(self.ui.noteMVC.updateKeywordFilter)
        self.ui.notebookMVC.addNewNote.connect(self.handleNewNote)
        self.ui.notebookMVC.addNewNotebook.connect(self.handleNewNotebook)
        self.ui.notebookMVC.selectedNotebooksChanged.connect(self.ui.noteMVC.updateNotebookFilter)
        self.ui.noteMVC.addNewNote.connect(self.handleNewNote)
        self.ui.noteMVC.copyNote.connect(self.handleCopyNote)
        self.ui.noteMVC.editNote.connect(self.handleEditNote)
        self.ui.noteMVC.moveNote.connect(self.handleMoveNote)
        self.ui.noteMVC.noteKeywordsChanged.connect(self.ui.keywordChooserMVC.updateKeywords)
        self.ui.noteMVC.selectedNoteChanged.connect(self.viewer.newNoteView)

        self.viewer.editNote.connect(self.handleEditNote)
        self.viewer.noteLinkClicked.connect(self.ui.noteMVC.handleNoteLinkClicked)

        self.loadNotebooks()

        # Check that we have a valid identity for git commits.
        if (self.settings.value("username", "") == ""):
            # FIXME: Use a timer so that this dialog appears after the main window is displayed.
            self.handleChangeIdentity(True)
        else:
            self.username = str(self.settings.value("username"))
            self.email = str(self.settings.value("email"))

    @logger.logFn
    def closeEvent(self, event):

        # If we put anything on the clipboard, clear it before exitting.
        clipboard = QtWidgets.QApplication.clipboard()
        if clipboard.ownsClipboard():
            clipboard.clear()
        
        self.settings.setValue("directory", self.directory)
        self.settings.setValue("main_window.pos", self.pos())
        self.settings.setValue("main_window.size", self.size())
        self.settings.setValue("main_splitter", self.ui.mainSplitter.saveState())
        self.settings.setValue("notebook_splitter", self.ui.notebookSplitter.saveState())

    @logger.logFn        
    def handleChangeIdentity(self, boolean):
        [self.username, self.email] = misc.getUserInfo(self.username, self.email)
        self.settings.setValue("username", self.username)
        self.settings.setValue("email", self.email)

    @logger.logFn
    def handleCopyNote(self, a_note):
        nb = notebook.chooseNotebook(self.ui.notebookMVC)
        if nb is not None:
            self.ui.noteMVC.copyANote(nb, a_note)
        
    @logger.logFn
    def handleEditNote(self, a_note, note_content):
        ok = True
        if not a_note.isLatestVersion(note_content):
            reply = QtWidgets.QMessageBox.warning(self,
                                                  'Warning',
                                                  'This is not the latest version of this note, edit anyway?',
                                                  QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if (reply == QtWidgets.QMessageBox.Yes):
                ok = True
            else:
                ok = False
        if ok:
            temp = a_note.getEditor()
            if temp is not None:
                temp.getEditor().raise_()
            else:
                temp = editor.Editor(a_note, note_content, parent = self)
                a_note.setEditor(temp)
                temp.show()
            temp.noteSaved.connect(self.ui.noteMVC.updateNoteDisplay)

    @logger.logFn
    def handleMoveNote(self, a_note):
        nb = notebook.chooseNotebook(self.ui.notebookMVC, a_note.getNotebook())
        if nb is not None:
            self.ui.noteMVC.moveANote(nb, a_note)
        
    @logger.logFn            
    def handleNewNote(self, nb = None):
        [name, ok] = QtWidgets.QInputDialog.getText(self,
                                                    'New Note',
                                                    'Enter the notes name:')        
        if ok:
            if not (isinstance(nb, notebook.NotebookStandardItem)):
                nb = notebook.chooseNotebook(self.ui.notebookMVC)
            if nb is not None:
                self.ui.noteMVC.addNote(nb, str(name))

    @logger.logFn
    def handleNewNotebook(self, boolean = False):
        [notebook_name, ok] = QtWidgets.QInputDialog.getText(self,
                                                             'New Notebook',
                                                             'Enter the notebooks name:')        
        if ok:
            self.ui.notebookMVC.addNotebook(self.directory, str(notebook_name), self.username, self.email)

    @logger.logFn            
    def handleSetDirectory(self, boolean):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                               "New Directory",
                                                               str(self.directory),
                                                               QtWidgets.QFileDialog.ShowDirsOnly)
        if directory:
            if (directory[-1] != "/"):
                directory += "/"
            print(directory)
            self.directory = directory
            self.ui.noteMVC.clearNotes()
            self.loadNotebooks()

    @logger.logFn
    def handleQuit(self, boolean):
        self.close()

    @logger.logFn        
    def loadNotebooks(self):
        self.ui.notebookMVC.loadNotebooks(self.directory)
        for nb in self.ui.notebookMVC.getAllNotebooks():
            self.ui.noteMVC.loadNotes(nb)
        

if (__name__ == "__main__"):
    app = QtWidgets.QApplication(sys.argv)

    window = APyEC()
    window.show()
    app.exec_()

