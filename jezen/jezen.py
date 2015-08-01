#!/usr/bin/env python

import os
import sys

from PyQt4 import QtCore, QtGui

import jezen_ui as jezenUi

import notebook


class Jezen(QtGui.QMainWindow):

    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.settings = QtCore.QSettings("jezen", "jezen")

        # Load UI
        self.ui = jezenUi.Ui_MainWindow()
        self.ui.setupUi(self)

        # Load settings
        self.directory = str(self.settings.value("directory", "./").toString())
        
        # Connect signals
        self.ui.actionNew_Note.triggered.connect(self.handleNewNote)
        self.ui.actionNew_Notebook.triggered.connect(self.handleNewNotebook)
        self.ui.actionSet_Directory.triggered.connect(self.handleSetDirectory)
        self.ui.actionQuit.triggered.connect(self.handleQuit)

        # Start
        self.loadNotebooks()
        
    def closeEvent(self, event):
        self.settings.setValue("directory", self.directory)

    def handleNewNote(self, boolean):
        [name, ok] = QtGui.QInputDialog.getText(self,
                                                'New Note',
                                                'Enter the notes name:')        
        if ok:
            nb = notebook.chooseNotebook(self.ui.notebookMVC)
            if nb is not None:
                self.ui.noteMVC.addNote(nb, str(name))
        
    def handleNewNotebook(self, boolean):
        [name, ok] = QtGui.QInputDialog.getText(self,
                                                'New Notebook',
                                                'Enter the notebooks name:')        
        if ok:
            self.ui.notebookMVC.addNotebook(self.directory, str(name))
        
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

