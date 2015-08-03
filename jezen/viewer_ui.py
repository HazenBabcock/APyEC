# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewer.ui'
#
# Created: Mon Aug  3 18:22:26 2015
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
        Form.resize(639, 733)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.webViewWidget = QtGui.QWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.webViewWidget.sizePolicy().hasHeightForWidth())
        self.webViewWidget.setSizePolicy(sizePolicy)
        self.webViewWidget.setObjectName(_fromUtf8("webViewWidget"))
        self.verticalLayout.addWidget(self.webViewWidget)
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
        self.versionLabel.setText(_translate("Form", "Versions:", None))
        self.editPushButton.setText(_translate("Form", "Edit", None))

