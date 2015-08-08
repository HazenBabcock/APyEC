# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editor.ui'
#
# Created: Sat Aug  8 15:58:27 2015
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1177, 850)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.viewEditSplitter = QtGui.QSplitter(Dialog)
        self.viewEditSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.viewEditSplitter.setObjectName(_fromUtf8("viewEditSplitter"))
        self.noteGroupBox = QtGui.QGroupBox(self.viewEditSplitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noteGroupBox.sizePolicy().hasHeightForWidth())
        self.noteGroupBox.setSizePolicy(sizePolicy)
        self.noteGroupBox.setObjectName(_fromUtf8("noteGroupBox"))
        self.editSplitter = QtGui.QSplitter(self.viewEditSplitter)
        self.editSplitter.setOrientation(QtCore.Qt.Vertical)
        self.editSplitter.setObjectName(_fromUtf8("editSplitter"))
        self.markdownGroupBox = QtGui.QGroupBox(self.editSplitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.markdownGroupBox.sizePolicy().hasHeightForWidth())
        self.markdownGroupBox.setSizePolicy(sizePolicy)
        self.markdownGroupBox.setObjectName(_fromUtf8("markdownGroupBox"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.markdownGroupBox)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.noteTextEdit = QtGui.QTextEdit(self.markdownGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noteTextEdit.sizePolicy().hasHeightForWidth())
        self.noteTextEdit.setSizePolicy(sizePolicy)
        self.noteTextEdit.setObjectName(_fromUtf8("noteTextEdit"))
        self.verticalLayout_5.addWidget(self.noteTextEdit)
        self.keywordSplitter = QtGui.QSplitter(self.editSplitter)
        self.keywordSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.keywordSplitter.setObjectName(_fromUtf8("keywordSplitter"))
        self.attachmentsGroupBox = QtGui.QGroupBox(self.keywordSplitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.attachmentsGroupBox.sizePolicy().hasHeightForWidth())
        self.attachmentsGroupBox.setSizePolicy(sizePolicy)
        self.attachmentsGroupBox.setObjectName(_fromUtf8("attachmentsGroupBox"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.attachmentsGroupBox)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.attachmentsMVC = AttachmentsMVC(self.attachmentsGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.attachmentsMVC.sizePolicy().hasHeightForWidth())
        self.attachmentsMVC.setSizePolicy(sizePolicy)
        self.attachmentsMVC.setObjectName(_fromUtf8("attachmentsMVC"))
        self.verticalLayout_4.addWidget(self.attachmentsMVC)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.attachUploadButton = QtGui.QPushButton(self.attachmentsGroupBox)
        self.attachUploadButton.setObjectName(_fromUtf8("attachUploadButton"))
        self.horizontalLayout.addWidget(self.attachUploadButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.keywordEditGroupBox = QtGui.QGroupBox(self.keywordSplitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.keywordEditGroupBox.sizePolicy().hasHeightForWidth())
        self.keywordEditGroupBox.setSizePolicy(sizePolicy)
        self.keywordEditGroupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.keywordEditGroupBox.setObjectName(_fromUtf8("keywordEditGroupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.keywordEditGroupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.keywordEditorMVC = KeywordEditorMVC(self.keywordEditGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.keywordEditorMVC.sizePolicy().hasHeightForWidth())
        self.keywordEditorMVC.setSizePolicy(sizePolicy)
        self.keywordEditorMVC.setObjectName(_fromUtf8("keywordEditorMVC"))
        self.verticalLayout.addWidget(self.keywordEditorMVC)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.keywordLineEdit = QtGui.QLineEdit(self.keywordEditGroupBox)
        self.keywordLineEdit.setObjectName(_fromUtf8("keywordLineEdit"))
        self.horizontalLayout_3.addWidget(self.keywordLineEdit)
        self.keywordAddPushButton = QtGui.QPushButton(self.keywordEditGroupBox)
        self.keywordAddPushButton.setObjectName(_fromUtf8("keywordAddPushButton"))
        self.horizontalLayout_3.addWidget(self.keywordAddPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addWidget(self.viewEditSplitter)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.saveButton = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setAutoDefault(False)
        self.saveButton.setDefault(False)
        self.saveButton.setFlat(False)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.horizontalLayout_2.addWidget(self.saveButton)
        self.closeButton = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.closeButton.sizePolicy().hasHeightForWidth())
        self.closeButton.setSizePolicy(sizePolicy)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout_2.addWidget(self.closeButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Jezen Note Editor", None))
        self.noteGroupBox.setTitle(_translate("Dialog", "Note", None))
        self.markdownGroupBox.setTitle(_translate("Dialog", "Content", None))
        self.attachmentsGroupBox.setTitle(_translate("Dialog", "Attachments", None))
        self.attachUploadButton.setText(_translate("Dialog", "Upload", None))
        self.keywordEditGroupBox.setTitle(_translate("Dialog", "Keywords", None))
        self.keywordAddPushButton.setText(_translate("Dialog", "Add", None))
        self.saveButton.setText(_translate("Dialog", "Save", None))
        self.closeButton.setText(_translate("Dialog", "Close", None))

from keywords import KeywordEditorMVC
from attachments import AttachmentsMVC
