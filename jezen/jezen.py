#!/usr/bin/env python

import sys

from PyQt4 import QtCore, QtGui

import jezen_ui as jezenUi

class Jezen(QtGui.QMainWindow):

    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.settings = QtCore.QSettings("jezen", "jezen")

        # Load UI
        self.ui = jezenUi.Ui_MainWindow()
        self.ui.setupUi(self)

        # Load settings
        self.directory = self.settings.value("directory", "./").toString()
        
        # Connect signals
        self.ui.actionSet_Directory.triggered.connect(self.handleSetDirectory)
        self.ui.actionQuit.triggered.connect(self.handleQuit)

        # Start
        self.loadNotebooks()
        
    def closeEvent(self, event):
        self.settings.setValue("directory", self.directory)

    def handleSetDirectory(self):
        directory = str(QtGui.QFileDialog.getExistingDirectory(self,
                                                               "New Directory",
                                                               str(self.directory),
                                                               QtGui.QFileDialog.ShowDirsOnly))
        if directory:
            print directory
            self.directory = directory
            self.loadNotebooks()
        
    def handleQuit(self):
        self.close()

    def loadNotebooks(self):
        pass
    

if (__name__ == "__main__"):
    app = QtGui.QApplication(sys.argv)

    window = Jezen()
    window.show()
    app.exec_()

