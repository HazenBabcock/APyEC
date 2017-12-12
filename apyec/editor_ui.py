# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editor.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1177, 850)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.viewEditSplitter = QtWidgets.QSplitter(Dialog)
        self.viewEditSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.viewEditSplitter.setObjectName("viewEditSplitter")
        self.noteGroupBox = QtWidgets.QGroupBox(self.viewEditSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noteGroupBox.sizePolicy().hasHeightForWidth())
        self.noteGroupBox.setSizePolicy(sizePolicy)
        self.noteGroupBox.setObjectName("noteGroupBox")
        self.editSplitter = QtWidgets.QSplitter(self.viewEditSplitter)
        self.editSplitter.setOrientation(QtCore.Qt.Vertical)
        self.editSplitter.setObjectName("editSplitter")
        self.layoutWidget = QtWidgets.QWidget(self.editSplitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.markdownGroupBox = QtWidgets.QGroupBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.markdownGroupBox.sizePolicy().hasHeightForWidth())
        self.markdownGroupBox.setSizePolicy(sizePolicy)
        self.markdownGroupBox.setObjectName("markdownGroupBox")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.markdownGroupBox)
        self.verticalLayout_5.setContentsMargins(2, -1, 2, 2)
        self.verticalLayout_5.setSpacing(2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.noteTextEdit = NoteTextEdit(self.markdownGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noteTextEdit.sizePolicy().hasHeightForWidth())
        self.noteTextEdit.setSizePolicy(sizePolicy)
        self.noteTextEdit.setFrameShape(QtWidgets.QFrame.Box)
        self.noteTextEdit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.noteTextEdit.setTabStopWidth(20)
        self.noteTextEdit.setObjectName("noteTextEdit")
        self.verticalLayout_5.addWidget(self.noteTextEdit)
        self.verticalLayout_2.addWidget(self.markdownGroupBox)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.contentTypeLabel = QtWidgets.QLabel(self.layoutWidget)
        self.contentTypeLabel.setObjectName("contentTypeLabel")
        self.horizontalLayout_4.addWidget(self.contentTypeLabel)
        self.contentTypeComboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.contentTypeComboBox.setObjectName("contentTypeComboBox")
        self.horizontalLayout_4.addWidget(self.contentTypeComboBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.keywordSplitter = QtWidgets.QSplitter(self.editSplitter)
        self.keywordSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.keywordSplitter.setObjectName("keywordSplitter")
        self.attachmentsGroupBox = QtWidgets.QGroupBox(self.keywordSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.attachmentsGroupBox.sizePolicy().hasHeightForWidth())
        self.attachmentsGroupBox.setSizePolicy(sizePolicy)
        self.attachmentsGroupBox.setObjectName("attachmentsGroupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.attachmentsGroupBox)
        self.verticalLayout_4.setContentsMargins(2, -1, 2, 2)
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.attachmentsMVC = AttachmentsMVC(self.attachmentsGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.attachmentsMVC.sizePolicy().hasHeightForWidth())
        self.attachmentsMVC.setSizePolicy(sizePolicy)
        self.attachmentsMVC.setFrameShape(QtWidgets.QFrame.Box)
        self.attachmentsMVC.setFrameShadow(QtWidgets.QFrame.Plain)
        self.attachmentsMVC.setObjectName("attachmentsMVC")
        self.verticalLayout_4.addWidget(self.attachmentsMVC)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.attachUploadButton = QtWidgets.QPushButton(self.attachmentsGroupBox)
        self.attachUploadButton.setObjectName("attachUploadButton")
        self.horizontalLayout.addWidget(self.attachUploadButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.keywordEditGroupBox = QtWidgets.QGroupBox(self.keywordSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.keywordEditGroupBox.sizePolicy().hasHeightForWidth())
        self.keywordEditGroupBox.setSizePolicy(sizePolicy)
        self.keywordEditGroupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.keywordEditGroupBox.setObjectName("keywordEditGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.keywordEditGroupBox)
        self.verticalLayout.setContentsMargins(2, -1, 2, 2)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.keywordEditorMVC = KeywordEditorMVC(self.keywordEditGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.keywordEditorMVC.sizePolicy().hasHeightForWidth())
        self.keywordEditorMVC.setSizePolicy(sizePolicy)
        self.keywordEditorMVC.setFrameShape(QtWidgets.QFrame.Box)
        self.keywordEditorMVC.setFrameShadow(QtWidgets.QFrame.Plain)
        self.keywordEditorMVC.setObjectName("keywordEditorMVC")
        self.verticalLayout.addWidget(self.keywordEditorMVC)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.keywordLineEdit = QtWidgets.QLineEdit(self.keywordEditGroupBox)
        self.keywordLineEdit.setObjectName("keywordLineEdit")
        self.horizontalLayout_3.addWidget(self.keywordLineEdit)
        self.keywordAddPushButton = QtWidgets.QPushButton(self.keywordEditGroupBox)
        self.keywordAddPushButton.setObjectName("keywordAddPushButton")
        self.horizontalLayout_3.addWidget(self.keywordAddPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addWidget(self.viewEditSplitter)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.saveButton = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setAutoDefault(False)
        self.saveButton.setDefault(False)
        self.saveButton.setFlat(False)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_2.addWidget(self.saveButton)
        self.closeButton = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.closeButton.sizePolicy().hasHeightForWidth())
        self.closeButton.setSizePolicy(sizePolicy)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout_2.addWidget(self.closeButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "APyEC Note Editor"))
        self.noteGroupBox.setTitle(_translate("Dialog", "Note"))
        self.markdownGroupBox.setTitle(_translate("Dialog", "Content"))
        self.contentTypeLabel.setText(_translate("Dialog", "Content Type:"))
        self.attachmentsGroupBox.setTitle(_translate("Dialog", "Attachments"))
        self.attachUploadButton.setText(_translate("Dialog", "Upload"))
        self.keywordEditGroupBox.setTitle(_translate("Dialog", "Keywords"))
        self.keywordAddPushButton.setText(_translate("Dialog", "Add"))
        self.saveButton.setText(_translate("Dialog", "Save"))
        self.closeButton.setText(_translate("Dialog", "Close"))

from attachments import AttachmentsMVC
from keywords import KeywordEditorMVC
from noteTextEdit import NoteTextEdit
