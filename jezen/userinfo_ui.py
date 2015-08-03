# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'userinfo.ui'
#
# Created: Sun Aug  2 15:27:05 2015
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
        Dialog.resize(409, 142)
        Dialog.setMaximumSize(QtCore.QSize(16777215, 142))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.usernameLabel = QtGui.QLabel(Dialog)
        self.usernameLabel.setObjectName(_fromUtf8("usernameLabel"))
        self.horizontalLayout.addWidget(self.usernameLabel)
        self.usernameLineEdit = QtGui.QLineEdit(Dialog)
        self.usernameLineEdit.setObjectName(_fromUtf8("usernameLineEdit"))
        self.horizontalLayout.addWidget(self.usernameLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.emailLabel = QtGui.QLabel(Dialog)
        self.emailLabel.setObjectName(_fromUtf8("emailLabel"))
        self.horizontalLayout_2.addWidget(self.emailLabel)
        self.emailLineEdit = QtGui.QLineEdit(Dialog)
        self.emailLineEdit.setObjectName(_fromUtf8("emailLineEdit"))
        self.horizontalLayout_2.addWidget(self.emailLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_3.setText(_translate("Dialog", "User Identification (for git)", None))
        self.usernameLabel.setText(_translate("Dialog", "User name", None))
        self.emailLabel.setText(_translate("Dialog", "Email address", None))

