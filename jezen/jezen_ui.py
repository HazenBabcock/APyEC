# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'jezen.ui'
#
# Created: Sat Aug  1 15:19:36 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1088, 531)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.mainSplitter = QtGui.QSplitter(self.centralwidget)
        self.mainSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.mainSplitter.setObjectName(_fromUtf8("mainSplitter"))
        self.notebookSplitter = QtGui.QSplitter(self.mainSplitter)
        self.notebookSplitter.setOrientation(QtCore.Qt.Vertical)
        self.notebookSplitter.setObjectName(_fromUtf8("notebookSplitter"))
        self.notebookGroupBox = QtGui.QGroupBox(self.notebookSplitter)
        self.notebookGroupBox.setObjectName(_fromUtf8("notebookGroupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.notebookGroupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.notebookMVC = NotebookMVC(self.notebookGroupBox)
        self.notebookMVC.setObjectName(_fromUtf8("notebookMVC"))
        self.verticalLayout.addWidget(self.notebookMVC)
        self.keywordGroupBox = QtGui.QGroupBox(self.notebookSplitter)
        self.keywordGroupBox.setObjectName(_fromUtf8("keywordGroupBox"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.keywordGroupBox)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.keywordsListView = QtGui.QListView(self.keywordGroupBox)
        self.keywordsListView.setObjectName(_fromUtf8("keywordsListView"))
        self.verticalLayout_3.addWidget(self.keywordsListView)
        self.notesGroupBox = QtGui.QGroupBox(self.mainSplitter)
        self.notesGroupBox.setObjectName(_fromUtf8("notesGroupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.notesGroupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.noteMVC = NoteMVC(self.notesGroupBox)
        self.noteMVC.setObjectName(_fromUtf8("noteMVC"))
        self.verticalLayout_2.addWidget(self.noteMVC)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.sortbyLabel = QtGui.QLabel(self.notesGroupBox)
        self.sortbyLabel.setObjectName(_fromUtf8("sortbyLabel"))
        self.horizontalLayout_4.addWidget(self.sortbyLabel)
        self.sortbyCcomboBox = QtGui.QComboBox(self.notesGroupBox)
        self.sortbyCcomboBox.setObjectName(_fromUtf8("sortbyCcomboBox"))
        self.horizontalLayout_4.addWidget(self.sortbyCcomboBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.viewEditTabWidget = QtGui.QTabWidget(self.mainSplitter)
        self.viewEditTabWidget.setObjectName(_fromUtf8("viewEditTabWidget"))
        self.viewTab = QtGui.QWidget()
        self.viewTab.setObjectName(_fromUtf8("viewTab"))
        self.viewEditTabWidget.addTab(self.viewTab, _fromUtf8(""))
        self.horizontalLayout_3.addWidget(self.mainSplitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1088, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew_Notebook = QtGui.QAction(MainWindow)
        self.actionNew_Notebook.setObjectName(_fromUtf8("actionNew_Notebook"))
        self.actionSet_Directory = QtGui.QAction(MainWindow)
        self.actionSet_Directory.setObjectName(_fromUtf8("actionSet_Directory"))
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionNew_Note = QtGui.QAction(MainWindow)
        self.actionNew_Note.setObjectName(_fromUtf8("actionNew_Note"))
        self.actionPrint_Note = QtGui.QAction(MainWindow)
        self.actionPrint_Note.setObjectName(_fromUtf8("actionPrint_Note"))
        self.menuFile.addAction(self.actionNew_Note)
        self.menuFile.addAction(self.actionNew_Notebook)
        self.menuFile.addAction(self.actionPrint_Note)
        self.menuFile.addAction(self.actionSet_Directory)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.viewEditTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Jezen", None))
        self.notebookGroupBox.setTitle(_translate("MainWindow", "Note Books", None))
        self.keywordGroupBox.setTitle(_translate("MainWindow", "Key Words", None))
        self.notesGroupBox.setTitle(_translate("MainWindow", "Notes", None))
        self.sortbyLabel.setText(_translate("MainWindow", "Sort By:", None))
        self.viewEditTabWidget.setTabText(self.viewEditTabWidget.indexOf(self.viewTab), _translate("MainWindow", "View", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionNew_Notebook.setText(_translate("MainWindow", "New Notebook", None))
        self.actionSet_Directory.setText(_translate("MainWindow", "Set Directory", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))
        self.actionNew_Note.setText(_translate("MainWindow", "New Note", None))
        self.actionPrint_Note.setText(_translate("MainWindow", "Print Note", None))

from note import NoteMVC
from notebook import NotebookMVC
