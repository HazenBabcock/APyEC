#!/usr/bin/env python
"""
.. module:: editor
   :synopsis: The editor (and viewer) for notes.
"""

import markdown
import os
import uuid

from PyQt4 import QtCore, QtGui, QtWebKit

import editor_ui as editorUi
import viewer_ui as viewerUi

#
# FIXME:
#  Maybe someone else has already written something better than this?
#

class Editor(QtGui.QDialog):
    """
    Handles interaction with the ui.editTab
    """
    def __init__(self, note, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.note = note
        self.update_timer = QtCore.QTimer()

        self.update_timer.setInterval(200)
        self.update_timer.setSingleShot(True)
        
        self.ui = editorUi.Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.Window)
        
        self.ui.noteTextEdit.setText(self.note.getMarkdown())
                
        self.viewer = Viewer(self.ui.noteGroupBox)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.viewer)
        self.ui.noteGroupBox.setLayout(layout)

        self.ui.closeButton.clicked.connect(self.close)
        self.ui.noteTextEdit.textChanged.connect(self.handleTextChanged)
        self.ui.saveButton.clicked.connect(self.handleSave)
        self.update_timer.timeout.connect(self.handleUpdateTimer)

        self.handleUpdateTimer()
        
    def getMarkdown(self):
        return str(self.ui.noteTextEdit.toPlainText())

    # FIXME: Need to check if the note has changed to reduce spurious commits.
    def handleSave(self):
        self.note.setMarkdown(unicode(self.ui.noteTextEdit.toPlainText()))
        self.note.saveNote()

    def handleTextChanged(self):
        self.update_timer.start()
        
    def handleUpdateTimer(self):
        self.viewer.updateWebView(unicode(self.ui.noteTextEdit.toPlainText()))


class Viewer(QtGui.QWidget):
    """
    Handles interaction with a viewer form.
    """
    editNote = QtCore.pyqtSignal(object)
    noteLinkClicked = QtCore.pyqtSignal(str, int)
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.note = None

        self.ui = viewerUi.Ui_Form()
        self.ui.setupUi(self)
        
        self.web_viewer = QtWebKit.QWebView(self)
        self.web_viewer.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.web_viewer)
        self.ui.webViewWidget.setLayout(layout)

        self.ui.editPushButton.clicked.connect(self.handleEditButton)
        self.ui.versionComboBox.currentIndexChanged.connect(self.handleVersionChange)
        self.web_viewer.linkClicked.connect(self.handleLinkClicked)

        self.ui.versionWidget.hide()

    def handleEditButton(self):
        self.editNote.emit(self.note)

    def handleLinkClicked(self, url):
        url_string = url.toString()
        if (url_string[:4] == "note"):
            [note_name, note_version] = url.toString().split("&v=")
            self.noteLinkClicked.emit(note_name, int(note_version))

    def handleVersionChange(self, new_index):
        self.note.loadNote(new_index)
        self.updateWebView(self.note.getMarkdown())

    def newNote(self, new_note):
        self.note = new_note

        # Update markdown.
        self.updateWebView(self.note.getMarkdown())

        # Fill in version combo box.
        self.ui.versionComboBox.currentIndexChanged.disconnect()
        n_versions = self.note.getNumberOfVersions()
        self.ui.versionComboBox.clear()
        for i in range(n_versions):
            self.ui.versionComboBox.addItem(str(i+1))
        self.ui.versionComboBox.setCurrentIndex(self.note.getCurrentVersionNumber())
        self.ui.versionComboBox.currentIndexChanged.connect(self.handleVersionChange)
            
        # Show combo box and edit button (if they are hidden).
        self.ui.versionWidget.show()

    def updateWebView(self, mdown):

        html = markdown.markdown(mdown)

        # Update to references to point to the correct attachments.
        
        
        # Display.
        self.web_viewer.setHtml(html)

    
