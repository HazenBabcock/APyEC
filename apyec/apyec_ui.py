# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'apyec.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1177, 829)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.mainSplitter = QtWidgets.QSplitter(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainSplitter.sizePolicy().hasHeightForWidth())
        self.mainSplitter.setSizePolicy(sizePolicy)
        self.mainSplitter.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.mainSplitter.setFrameShadow(QtWidgets.QFrame.Plain)
        self.mainSplitter.setMidLineWidth(0)
        self.mainSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.mainSplitter.setObjectName("mainSplitter")
        self.notebookSplitter = QtWidgets.QSplitter(self.mainSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.notebookSplitter.sizePolicy().hasHeightForWidth())
        self.notebookSplitter.setSizePolicy(sizePolicy)
        self.notebookSplitter.setOrientation(QtCore.Qt.Vertical)
        self.notebookSplitter.setObjectName("notebookSplitter")
        self.notebookGroupBox = QtWidgets.QGroupBox(self.notebookSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.notebookGroupBox.sizePolicy().hasHeightForWidth())
        self.notebookGroupBox.setSizePolicy(sizePolicy)
        self.notebookGroupBox.setObjectName("notebookGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.notebookGroupBox)
        self.verticalLayout.setContentsMargins(2, 9, 2, 2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.notebookMVC = NotebookMVC(self.notebookGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.notebookMVC.sizePolicy().hasHeightForWidth())
        self.notebookMVC.setSizePolicy(sizePolicy)
        self.notebookMVC.setFrameShape(QtWidgets.QFrame.Box)
        self.notebookMVC.setFrameShadow(QtWidgets.QFrame.Plain)
        self.notebookMVC.setObjectName("notebookMVC")
        self.verticalLayout.addWidget(self.notebookMVC)
        self.keywordGroupBox = QtWidgets.QGroupBox(self.notebookSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.keywordGroupBox.sizePolicy().hasHeightForWidth())
        self.keywordGroupBox.setSizePolicy(sizePolicy)
        self.keywordGroupBox.setObjectName("keywordGroupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.keywordGroupBox)
        self.verticalLayout_3.setContentsMargins(2, -1, 2, 2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.keywordChooserMVC = KeywordChooserMVC(self.keywordGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.keywordChooserMVC.sizePolicy().hasHeightForWidth())
        self.keywordChooserMVC.setSizePolicy(sizePolicy)
        self.keywordChooserMVC.setFrameShape(QtWidgets.QFrame.Box)
        self.keywordChooserMVC.setFrameShadow(QtWidgets.QFrame.Plain)
        self.keywordChooserMVC.setObjectName("keywordChooserMVC")
        self.verticalLayout_3.addWidget(self.keywordChooserMVC)
        self.notesGroupBox = QtWidgets.QGroupBox(self.mainSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.notesGroupBox.sizePolicy().hasHeightForWidth())
        self.notesGroupBox.setSizePolicy(sizePolicy)
        self.notesGroupBox.setObjectName("notesGroupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.notesGroupBox)
        self.verticalLayout_2.setContentsMargins(2, -1, 2, 2)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.noteMVC = NoteMVC(self.notesGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noteMVC.sizePolicy().hasHeightForWidth())
        self.noteMVC.setSizePolicy(sizePolicy)
        self.noteMVC.setFrameShape(QtWidgets.QFrame.Box)
        self.noteMVC.setFrameShadow(QtWidgets.QFrame.Plain)
        self.noteMVC.setObjectName("noteMVC")
        self.verticalLayout_2.addWidget(self.noteMVC)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.sortbyLabel = QtWidgets.QLabel(self.notesGroupBox)
        self.sortbyLabel.setObjectName("sortbyLabel")
        self.horizontalLayout_4.addWidget(self.sortbyLabel)
        self.sortbyComboBox = QtWidgets.QComboBox(self.notesGroupBox)
        self.sortbyComboBox.setObjectName("sortbyComboBox")
        self.horizontalLayout_4.addWidget(self.sortbyComboBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.noteGroupBox = QtWidgets.QGroupBox(self.mainSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noteGroupBox.sizePolicy().hasHeightForWidth())
        self.noteGroupBox.setSizePolicy(sizePolicy)
        self.noteGroupBox.setObjectName("noteGroupBox")
        self.horizontalLayout_3.addWidget(self.mainSplitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1177, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew_Notebook = QtWidgets.QAction(MainWindow)
        self.actionNew_Notebook.setObjectName("actionNew_Notebook")
        self.actionSet_Directory = QtWidgets.QAction(MainWindow)
        self.actionSet_Directory.setObjectName("actionSet_Directory")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionNew_Note = QtWidgets.QAction(MainWindow)
        self.actionNew_Note.setObjectName("actionNew_Note")
        self.actionPrint_Note = QtWidgets.QAction(MainWindow)
        self.actionPrint_Note.setObjectName("actionPrint_Note")
        self.menuFile.addAction(self.actionNew_Note)
        self.menuFile.addAction(self.actionNew_Notebook)
        self.menuFile.addAction(self.actionPrint_Note)
        self.menuFile.addAction(self.actionSet_Directory)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "APyEC"))
        self.notebookGroupBox.setTitle(_translate("MainWindow", "Note Books"))
        self.keywordGroupBox.setTitle(_translate("MainWindow", "Key Words"))
        self.notesGroupBox.setTitle(_translate("MainWindow", "Notes"))
        self.sortbyLabel.setText(_translate("MainWindow", "Sort By:"))
        self.noteGroupBox.setTitle(_translate("MainWindow", "Note"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionNew_Notebook.setText(_translate("MainWindow", "New Notebook"))
        self.actionSet_Directory.setText(_translate("MainWindow", "Set Directory"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionNew_Note.setText(_translate("MainWindow", "New Note"))
        self.actionPrint_Note.setText(_translate("MainWindow", "Print Note"))

from keywords import KeywordChooserMVC
from note import NoteMVC
from notebook import NotebookMVC
