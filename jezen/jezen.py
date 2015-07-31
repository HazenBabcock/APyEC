#!/usr/bin/env python

import glob
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
        self.ui.actionNew_Notebook.triggered.connect(self.handleNewNotebook)
        self.ui.actionSet_Directory.triggered.connect(self.handleSetDirectory)
        self.ui.actionQuit.triggered.connect(self.handleQuit)

        # Start
        self.loadNotebooks()
        
    def closeEvent(self, event):
        self.settings.setValue("directory", self.directory)

    def handleNewNotebook(self):
        [name, ok] = QtGui.QInputDialog.getText(self,
                                                'New Notebook',
                                                'Enter the notebooks name:')        
        if ok:
            nb = notebook.NoteBook(self.directory, nb_name = str(name))
            self.ui.noteBookMVC.addNotebook(nb)
        
    def handleSetDirectory(self):
        directory = str(QtGui.QFileDialog.getExistingDirectory(self,
                                                               "New Directory",
                                                               str(self.directory),
                                                               QtGui.QFileDialog.ShowDirsOnly))
        if directory:
            if (directory[-1] != "/"):
                directory += "/"
            print directory
            self.directory = directory
            self.loadNotebooks()
        
    def handleQuit(self):
        self.close()

    def loadNotebooks(self):
        
        # Load individual notebooks.
        self.ui.noteBookMVC.loadNotebooks(map(lambda(x): notebook.NoteBook(self.directory, nb_uuid = x[len(self.directory) + 3:]),
                                              glob.glob(self.directory + "nb_*")))
        

if (__name__ == "__main__"):
    app = QtGui.QApplication(sys.argv)

    window = Jezen()
    window.show()
    app.exec_()

