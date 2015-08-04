#!/usr/bin/env python

import os
import sys

from PyQt4 import QtCore, QtGui

import jezen_ui as jezenUi

import editor
import misc
import notebook


class Jezen(QtGui.QMainWindow):

    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.email = ""
        self.settings = QtCore.QSettings("jezen", "jezen")
        self.username = ""

        # Load UI
        self.ui = jezenUi.Ui_MainWindow()
        self.ui.setupUi(self)

        self.viewer = editor.Viewer(self.ui.noteGroupBox)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.viewer)
        self.ui.noteGroupBox.setLayout(layout)

        # Load settings
        self.directory = str(self.settings.value("directory", "./").toString())

        # Restore geometry
        self.restoreGeometry(self.settings.value("main_window").toByteArray())
        self.ui.mainSplitter.restoreState(self.settings.value("main_splitter").toByteArray())
        self.ui.notebookSplitter.restoreState(self.settings.value("notebook_splitter").toByteArray())
            
        # Connect signals
        self.ui.actionNew_Note.triggered.connect(self.handleNewNote)
        self.ui.actionNew_Notebook.triggered.connect(self.handleNewNotebook)
        self.ui.actionSet_Directory.triggered.connect(self.handleSetDirectory)
        self.ui.actionQuit.triggered.connect(self.handleQuit)

        self.ui.notebookMVC.addNote.connect(self.handleNewNote)
        self.ui.notebookMVC.selectedNotebooksChanged.connect(self.ui.noteMVC.updateNotebookFilter)
        
        self.ui.noteMVC.selectedNoteChanged.connect(self.viewer.newNote)

        self.viewer.editNote.connect(self.handleEditNote)
        self.viewer.noteLinkClicked.connect(self.ui.noteMVC.handleNoteLinkClicked)

        self.loadNotebooks()

        # Check that we have a valid identity for git commits.
        if self.settings.value("username", None).isNull():
            # FIXME: Use a timer so that this dialog appears after the main window is displayed.
            self.handleChangeIdentity(True)
        else:
            self.username = str(self.settings.value("username", None).toString())
            self.email = str(self.settings.value("email", None).toString())
            
    def closeEvent(self, event):
        self.settings.setValue("directory", self.directory)
        self.settings.setValue("main_window", self.saveGeometry())
        self.settings.setValue("main_splitter", self.ui.mainSplitter.saveState())
        self.settings.setValue("notebook_splitter", self.ui.notebookSplitter.saveState())

    def handleChangeIdentity(self, boolean):
        [self.username, self.email] = misc.getUserInfo(self.username, self.email)
        self.settings.setValue("username", self.username)
        self.settings.setValue("email", self.email)

    def handleEditNote(self, a_note):
        ok = True
        if not a_note.isLatestVersion():
            reply = QtGui.QMessageBox.warning(self,
                                              'Warning',
                                              'This is not the latest version of this note, edit anyway?',
                                              QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if (reply == QtGui.QMessageBox.Yes):
                ok = True
            else:
                ok = False
        if ok:
            tmp = editor.Editor(a_note, self)
            tmp.show()
                       
    def handleNewNote(self, nb):
        [name, ok] = QtGui.QInputDialog.getText(self,
                                                'New Note',
                                                'Enter the notes name:')        
        if ok:
            if not (isinstance(nb, notebook.NotebookStandardItem)):
                nb = notebook.chooseNotebook(self.ui.notebookMVC)
            if nb is not None:
                self.ui.noteMVC.addNote(nb, str(name))
        
    def handleNewNotebook(self, boolean):
        [notebook_name, ok] = QtGui.QInputDialog.getText(self,
                                                         'New Notebook',
                                                         'Enter the notebooks name:')        
        if ok:
            self.ui.notebookMVC.addNotebook(self.directory, str(notebook_name), self.username, self.email)
        
    def handleSetDirectory(self, boolean):
        directory = str(QtGui.QFileDialog.getExistingDirectory(self,
                                                               "New Directory",
                                                               str(self.directory),
                                                               QtGui.QFileDialog.ShowDirsOnly))
        if directory:
            if (directory[-1] != "/"):
                directory += "/"
            print directory
            self.directory = directory
            self.ui.noteMVC.clearNotes()
            self.loadNotebooks()
        
    def handleQuit(self):
        self.close()

    def loadNotebooks(self):
        self.ui.notebookMVC.loadNotebooks(self.directory)
        for nb in self.ui.notebookMVC.getAllNotebooks():
            self.ui.noteMVC.loadNotes(nb)
        

if (__name__ == "__main__"):
    app = QtGui.QApplication(sys.argv)

    window = Jezen()
    window.show()
    app.exec_()

