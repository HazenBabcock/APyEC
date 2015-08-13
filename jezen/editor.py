#!/usr/bin/env python
"""
.. module:: editor
   :synopsis: The editor (and viewer) for notes.
"""

import os

from PyQt4 import QtCore, QtGui, QtWebKit

import editor_ui as editorUi
import viewer_ui as viewerUi

import logger

#
# FIXME:
#  Maybe someone else has already written a better editor (and viewer) than this?
#

class Editor(QtGui.QDialog):
    """
    Handles interaction with the ui.editTab
    """
    @logger.logFn
    def __init__(self, note, note_content, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.note = note
        self.note_content = note_content
        self.settings = QtCore.QSettings("jezen", "jezen")

        self.attach_directory = str(self.settings.value("attach_directory", ".").toString())
        
        # Note editting timer, to reduce the number of update
        # events when the user is typing.
        self.update_timer = QtCore.QTimer(self)
        self.update_timer.setInterval(200)
        self.update_timer.setSingleShot(True)

        self.ui = editorUi.Ui_Dialog()
        self.ui.setupUi(self)

        # This lets the edit window go behind the main window.
        self.setWindowFlags(QtCore.Qt.Window)
        
        self.ui.attachmentsMVC.newNote(self.note, self.note_content)
        self.ui.noteTextEdit.setText(self.note_content.getContent())
        self.ui.keywordEditorMVC.addKeywords(self.note_content.getKeywords())

        # Restore Geometry.
        self.restoreGeometry(self.settings.value("edit_dialog").toByteArray())
        self.ui.editSplitter.restoreState(self.settings.value("edit_splitter").toByteArray())
        self.ui.keywordSplitter.restoreState(self.settings.value("keyword_splitter").toByteArray())
        self.ui.viewEditSplitter.restoreState(self.settings.value("view_edit_splitter").toByteArray())
        
        self.viewer = Viewer(self.ui.noteGroupBox)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.viewer)
        self.ui.noteGroupBox.setLayout(layout)
        self.viewer.newNoteEdit(note, note_content)

        # Connect signals.
        self.ui.attachUploadButton.clicked.connect(self.handleAttachUpload)
        self.ui.closeButton.clicked.connect(self.close)
        self.ui.keywordAddPushButton.clicked.connect(self.handleKeywordAdd)
        self.ui.noteTextEdit.textChanged.connect(self.handleTextChanged)
        self.ui.saveButton.clicked.connect(self.handleSave)
        self.update_timer.timeout.connect(self.handleUpdateTimer)

    @logger.logFn        
    def closeEvent(self, event):
        self.settings.setValue("edit_dialog", self.saveGeometry())
        self.settings.setValue("edit_splitter", self.ui.editSplitter.saveState())
        self.settings.setValue("keyword_splitter", self.ui.keywordSplitter.saveState())
        self.settings.setValue("view_edit_splitter", self.ui.viewEditSplitter.saveState())


    @logger.logFn        
    def getContent(self):
        return str(self.ui.noteTextEdit.toPlainText())

    @logger.logFn    
    def handleAttachUpload(self, boolean):
        upload_filename = QtGui.QFileDialog.getOpenFileName(self,
                                                            "Upload File",
                                                            self.attach_directory,
                                                            "*")
        if upload_filename:
            upload_filename = str(upload_filename)
            self.attach_directory = os.path.dirname(upload_filename)
            self.ui.attachmentsMVC.addAttachment(upload_filename)

    @logger.logFn
    def handleKeywordAdd(self, boolean):
        keyword_text = str(self.ui.keywordLineEdit.text())
        if (len(keyword_text) > 0):
            self.ui.keywordEditorMVC.addKeyword(keyword_text)
                         
    # FIXME: Need to check if the note has changed to reduce spurious commits?
    @logger.logFn
    def handleSave(self, boolean):
        self.note_content.setContent(unicode(self.ui.noteTextEdit.toPlainText()))
        self.note_content.setKeywords(self.ui.keywordEditorMVC.getAllKeywords())
        self.note.saveNote(self.note_content)

    @logger.logFn        
    def handleTextChanged(self):
        self.update_timer.start()

    @logger.logFn        
    def handleUpdateTimer(self):
        self.viewer.updateWebView(unicode(self.ui.noteTextEdit.toPlainText()))


class Viewer(QtGui.QWidget):
    """
    Handles interaction with a viewer form.
    """
    editNote = QtCore.pyqtSignal(object, object)
    noteLinkClicked = QtCore.pyqtSignal(str, int)

    @logger.logFn    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.base_url = None
        self.note = None
        self.note_content = None

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

    @logger.logFn        
    def handleEditButton(self, boolean):
        self.editNote.emit(self.note, self.note_content)

    @logger.logFn        
    def handleLinkClicked(self, url):
        url_string = url.toString()
        if (url_string[:4] == "note"):
            [note_name, note_version] = url.toString().split("&v=")
            self.noteLinkClicked.emit(note_name, int(note_version))
        else:
            print url_string
            self.web_viewer.load(url)

    @logger.logFn
    def handleVersionChange(self, new_index):
        self.note_content = self.note.loadNoteContent(new_index)
        self.updateWebView(self.note_content.getContent())

    @logger.logFn
    def newNoteView(self, new_note):
        """
        Called when used directly as a viewer.
        """
        if new_note is None:
            self.web_viewer.setHtml("")
            self.ui.versionWidget.hide()
            return
            
        self.note = new_note
        self.base_url = QtCore.QUrl.fromLocalFile(self.note.getNotebook().getDirectory() + "notebook.xml")
        
        # Update content.
        n_versions = self.note.getNumberOfVersions()
        self.note_content = self.note.loadNoteContent(n_versions - 1)
        self.updateWebView(self.note_content.getContent())

        # Fill in version combo box.
        if (n_versions > 0):
            self.ui.versionComboBox.currentIndexChanged.disconnect()
            self.ui.versionComboBox.clear()
            for i in range(n_versions):
                self.ui.versionComboBox.addItem(str(i+1))
            self.ui.versionComboBox.setCurrentIndex(self.note_content.getVersionNumber())
            self.ui.versionComboBox.currentIndexChanged.connect(self.handleVersionChange)
            self.ui.versionComboBox.show()
        else:
            self.ui.versionComboBox.hide()
            
        # Show combo box and edit button (if they are hidden).
        self.ui.versionWidget.show()

    @logger.logFn
    def newNoteEdit(self, new_note, note_content):
        """
        Called when used to display a note in edit mode.
        """
        self.note = new_note
        self.note_content = note_content
        self.base_url = QtCore.QUrl.fromLocalFile(self.note.getNotebook().getDirectory() + "notebook.xml")

    @logger.logFn        
    def updateWebView(self, content):
        html = self.note_content.convertToHTML(content)
        
        # Display.
        self.web_viewer.setHtml(html, self.base_url)

    
