# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewer.ui'
#
# Created: Fri Aug 14 07:43:02 2015
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(495, 610)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 5, 0, 0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.keywordLabel = QtGui.QLabel(Form)
        self.keywordLabel.setObjectName(_fromUtf8("keywordLabel"))
        self.verticalLayout.addWidget(self.keywordLabel)
        self.webViewFrame = QtGui.QFrame(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.webViewFrame.sizePolicy().hasHeightForWidth())
        self.webViewFrame.setSizePolicy(sizePolicy)
        self.webViewFrame.setFrameShape(QtGui.QFrame.Box)
        self.webViewFrame.setObjectName(_fromUtf8("webViewFrame"))
        self.verticalLayout.addWidget(self.webViewFrame)
        self.versionWidget = QtGui.QWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.versionWidget.sizePolicy().hasHeightForWidth())
        self.versionWidget.setSizePolicy(sizePolicy)
        self.versionWidget.setObjectName(_fromUtf8("versionWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.versionWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.versionLabel = QtGui.QLabel(self.versionWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.versionLabel.sizePolicy().hasHeightForWidth())
        self.versionLabel.setSizePolicy(sizePolicy)
        self.versionLabel.setObjectName(_fromUtf8("versionLabel"))
        self.horizontalLayout.addWidget(self.versionLabel)
        self.versionComboBox = QtGui.QComboBox(self.versionWidget)
        self.versionComboBox.setObjectName(_fromUtf8("versionComboBox"))
        self.horizontalLayout.addWidget(self.versionComboBox)
        self.dateLabel = QtGui.QLabel(self.versionWidget)
        self.dateLabel.setObjectName(_fromUtf8("dateLabel"))
        self.horizontalLayout.addWidget(self.dateLabel)
        spacerItem = QtGui.QSpacerItem(374, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.editPushButton = QtGui.QPushButton(self.versionWidget)
        self.editPushButton.setObjectName(_fromUtf8("editPushButton"))
        self.horizontalLayout.addWidget(self.editPushButton)
        self.verticalLayout.addWidget(self.versionWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.keywordLabel.setText(_translate("Form", "Keywords:", None))
        self.versionLabel.setText(_translate("Form", "Versions:", None))
        self.dateLabel.setText(_translate("Form", "Date", None))
        self.editPushButton.setText(_translate("Form", "Edit", None))

