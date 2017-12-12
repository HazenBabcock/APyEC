# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewer.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(495, 625)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 5, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.keywordLabel = QtWidgets.QLabel(Form)
        self.keywordLabel.setObjectName("keywordLabel")
        self.verticalLayout.addWidget(self.keywordLabel)
        self.webViewFrame = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.webViewFrame.sizePolicy().hasHeightForWidth())
        self.webViewFrame.setSizePolicy(sizePolicy)
        self.webViewFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.webViewFrame.setObjectName("webViewFrame")
        self.verticalLayout.addWidget(self.webViewFrame)
        self.versionWidget = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.versionWidget.sizePolicy().hasHeightForWidth())
        self.versionWidget.setSizePolicy(sizePolicy)
        self.versionWidget.setObjectName("versionWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.versionWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.infoLabel = QtWidgets.QLabel(self.versionWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.infoLabel.sizePolicy().hasHeightForWidth())
        self.infoLabel.setSizePolicy(sizePolicy)
        self.infoLabel.setObjectName("infoLabel")
        self.horizontalLayout.addWidget(self.infoLabel)
        self.versionComboBox = QtWidgets.QComboBox(self.versionWidget)
        self.versionComboBox.setMinimumSize(QtCore.QSize(60, 0))
        self.versionComboBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.versionComboBox.setObjectName("versionComboBox")
        self.horizontalLayout.addWidget(self.versionComboBox)
        self.dateLabel = QtWidgets.QLabel(self.versionWidget)
        self.dateLabel.setObjectName("dateLabel")
        self.horizontalLayout.addWidget(self.dateLabel)
        spacerItem = QtWidgets.QSpacerItem(374, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.editPushButton = QtWidgets.QPushButton(self.versionWidget)
        self.editPushButton.setObjectName("editPushButton")
        self.horizontalLayout.addWidget(self.editPushButton)
        self.verticalLayout.addWidget(self.versionWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.keywordLabel.setText(_translate("Form", "Keywords:"))
        self.infoLabel.setText(_translate("Form", "Info"))
        self.dateLabel.setText(_translate("Form", "Date"))
        self.editPushButton.setText(_translate("Form", "Edit"))

