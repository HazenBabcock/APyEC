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

class Editor(QtGui.QWidget):
    """
    Handles interaction with the ui.editTab
    """
    saveNote = QtCore.pyqtSignal()
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.original_mdown = None

        self.ui = editorUi.Ui_Form()
        self.ui.setupUi(self)

        self.ui.saveButton.clicked.connect(self.handleSave)
        
    def getMarkdown(self):
        return str(self.ui.noteTextEdit.toPlainText())

    # FIXME: Need to check if the note has changed to reduce spurious commits.
    def handleSave(self):
        self.saveNote.emit()
        
    def setMarkdown(self, mdown):
        self.original_markdown = mdown
        self.ui.noteTextEdit.setText(mdown)

        
class EditorViewer(QtCore.QObject):
    """
    Handles interaction with the ui.viewEditTabWidget, where notes are
    editted and viewed.
    """
    def __init__(self, view_edit_tab_widget, parent = None):
        QtCore.QObject.__init__(self, parent)
        self.ve_tab_widget = view_edit_tab_widget
        self.note = None

        self.viewer = Viewer(self.note)
        self.ve_tab_widget.addTab(self.viewer, "View")

        self.editor = Editor(self.ve_tab_widget)
        self.ve_tab_widget.addTab(self.editor, "Edit")

        self.editor.saveNote.connect(self.handleSaveNote)
        self.ve_tab_widget.currentChanged.connect(self.handleTabChange)

    def handleSaveNote(self):
        if self.note is not None:
            self.note.setMarkdown(self.editor.getMarkdown())
            self.note.saveNote()
        
    def handleTabChange(self, new_tab):
        if (new_tab == 0):
            self.viewer.updateHTML(self.editor.getMarkdown())
        
    def newNote(self, note):
        self.note = note
        self.editor.setMarkdown(self.note.getMarkdown())
        self.viewer.updateHTML(self.note.getMarkdown())
        
        
class Viewer(QtGui.QWidget):
    """
    Handles interaction with the ui.viewTab
    """
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.note = None

        self.ui = viewerUi.Ui_Form()
        self.ui.setupUi(self)
        
        self.web_viewer = QtWebKit.QWebView(self)

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.web_viewer)
        self.ui.webViewWidget.setLayout(layout)

        self.ui.versionComboBox.currentIndexChanged.connect(self.handleVersionChange)            

        self.ui.versionWidget.hide()
        
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
        self.web_viewer.setHtml(markdown.markdown(mdown))

    
