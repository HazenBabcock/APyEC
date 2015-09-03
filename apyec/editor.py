#!/usr/bin/env python
"""
.. module:: editor
   :synopsis: The editor (and viewer) for notes.
"""

import datetime
import os
import webbrowser

from PyQt4 import QtCore, QtGui, QtWebKit

import editor_ui as editorUi
import viewer_ui as viewerUi

import converters
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
        self.settings = QtCore.QSettings("apyec", "apyec")

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
        layout.setMargin(2)
        layout.addWidget(self.viewer)
        self.ui.noteGroupBox.setLayout(layout)
        self.viewer.newNoteEdit(note, note_content)

        # Set up the content type combo box.
        for content_type in converters.content_types:
            self.ui.contentTypeComboBox.addItem(content_type)
        index = self.ui.contentTypeComboBox.findText(note_content.getContentType())
        if index >= 0:
            self.ui.contentTypeComboBox.setCurrentIndex(index)

        # Set up NoteTextEdit
        self.ui.noteTextEdit.setNoteContent(self.note_content)
        
        # Connect signals.
        self.ui.attachUploadButton.clicked.connect(self.handleAttachUpload)
        self.ui.closeButton.clicked.connect(self.close)
        self.ui.contentTypeComboBox.currentIndexChanged[str].connect(self.handleContentTypeChange)
        self.ui.keywordAddPushButton.clicked.connect(self.handleKeywordAdd)
        self.ui.noteTextEdit.textChanged.connect(self.handleTextChanged)
        self.ui.saveButton.clicked.connect(self.handleSave)
        self.update_timer.timeout.connect(self.handleUpdateTimer)

    @logger.logFn        
    def closeEvent(self, event):
        self.note.setEditor(None)
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
    def handleContentTypeChange(self, new_content_type):
        self.note_content.setContentType(new_content_type)
        
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
    noteLinkClicked = QtCore.pyqtSignal(str, str)

    @logger.logFn    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.base_url = None
        self.note = None
        self.note_content = None

        self.ui = viewerUi.Ui_Form()
        self.ui.setupUi(self)

        self.web_viewer = WebViewer(self)

        layout = QtGui.QHBoxLayout()
        layout.setMargin(2)
        layout.addWidget(self.web_viewer)
        self.ui.webViewFrame.setLayout(layout)

        self.ui.editPushButton.clicked.connect(self.handleEditButton)
        self.ui.versionComboBox.currentIndexChanged.connect(self.handleVersionChange)
        self.web_viewer.copyLink.connect(self.handleCopyLink)
        self.web_viewer.linkClicked.connect(self.handleLinkClicked)
        self.web_viewer.printNote.connect(self.handlePrint)

        self.ui.keywordLabel.hide()
        self.ui.versionWidget.hide()

    @logger.logFn
    def handleCopyLink(self):
        clipboard = QtGui.QApplication.clipboard()
        clipboard.setText("<note_link><split>" + self.note.getName() + "<split>" + self.note.getLink(self.note_content.getVersion()) + "<split></note_link>")
        
    @logger.logFn        
    def handleEditButton(self, boolean):
        self.editNote.emit(self.note, self.note_content)

    @logger.logFn
    def handleLinkClicked(self, url):
        url_string = url.toString()
        if (url_string[:6] == "apyec:"):
            [note_name, note_version] = url_string[7:].split("&v=")
            self.noteLinkClicked.emit(note_name, note_version)
        elif (url_string[:5] == "file:"):
            self.web_viewer.load(url)
        else:
            webbrowser.open(url_string)

    @logger.logFn
    def handlePrint(self, boolean):
        if self.note is not None:
            printer = QtGui.QPrinter()
            print_dialog = QtGui.QPrintDialog(printer, self)
            if (print_dialog.exec_() == QtGui.QDialog.Accepted):
                self.web_viewer.print_(printer)
        else:
            QtGui.QMessageBox.information(self,
                                          'Information',
                                          'No notes are currently selected.',
                                          QtGui.QMessageBox.Yes)
                
    @logger.logFn
    def handleVersionChange(self, new_index):
        version = str(self.ui.versionComboBox.itemData(new_index).toString())
        self.versionChange(version)

    @logger.logFn
    def newNoteView(self, new_note, version):
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
        if version is None:
            self.versionChange(self.note.getLatestVersion())
        else:
            self.versionChange(version)
            
        # Fill in version combo box.
        versions = self.note.getVersions()
        if (len(versions) > 1):
            self.ui.versionComboBox.currentIndexChanged.disconnect()
            self.ui.versionComboBox.clear()
            for i, v in enumerate(versions):
                self.ui.versionComboBox.addItem(str(i+1), v)
            cur_index = self.ui.versionComboBox.findData(self.note_content.getVersion())
            self.ui.versionComboBox.setCurrentIndex(cur_index)
            self.ui.versionComboBox.currentIndexChanged.connect(self.handleVersionChange)
            self.ui.versionComboBox.show()
        else:
            self.ui.versionLabel.hide()
            self.ui.versionComboBox.hide()
            
        # Show combo box and edit button (if they are hidden).
        self.ui.versionWidget.show()
        self.ui.keywordLabel.show()

    @logger.logFn
    def newNoteEdit(self, new_note, note_content):
        """
        Called when used to display a note in edit mode.
        """
        self.note = new_note
        self.note_content = note_content
        self.base_url = QtCore.QUrl.fromLocalFile(self.note.getNotebook().getDirectory() + "notebook.xml")
        self.updateWebView(self.note_content.getContent())

    @logger.logFn        
    def updateWebView(self, content):
        html = self.note_content.convertToHTML(content)
        
        # Display.
        self.web_viewer.setHtml(html, self.base_url)

    @logger.logFn
    def versionChange(self, version):
        self.note_content = self.note.loadNoteContent(version)
        self.updateWebView(self.note_content.getContent())
        self.ui.keywordLabel.setText("Keywords: " + ", ".join(self.note_content.getKeywords()))

        # Need to check that date is valid as newly created notes won't have a date.
        date = self.note_content.getDate()
        if date is not None:
            self.ui.dateLabel.setText(datetime.datetime.strftime(date, '%Y-%m-%d %H:%M:%S'))
        else:
            self.ui.dateLabel.setText("")        
    

class WebViewer(QtWebKit.QWebView):
    """
    Web viewer specialized for apyec.
    """
    copyLink = QtCore.pyqtSignal()
    printNote = QtCore.pyqtSignal(bool)
    
    def __init__(self, parent):
        QtWebKit.QWebView.__init__(self)
        self.have_content = False
        
        self.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)

        self.copyLinkAction = QtGui.QAction(self.tr("Copy Link to Clipboard"), self)
        self.copyLinkAction.triggered.connect(self.handleCopyLink)
        self.printNoteAction = QtGui.QAction(self.tr("Print"), self)
        self.printNoteAction.triggered.connect(self.handlePrintNote)

        self.webviewer_popup_menu = QtGui.QMenu(self)
        self.webviewer_popup_menu.addAction(self.copyLinkAction)
        self.webviewer_popup_menu.addAction(self.printNoteAction)

    @logger.logFn
    def contextMenuEvent(self, event):
        if self.have_content:
            self.webviewer_popup_menu.exec_(event.globalPos())
    
    @logger.logFn
    def handleCopyLink(self, boolean):
        self.copyLink.emit()

    @logger.logFn
    def handlePrintNote(self, boolean):
        self.printNote.emit(True)
        
    def setHtml(self, html, base_url = QtCore.QUrl()):
        self.have_content = True
        QtWebKit.QWebView.setHtml(self, html, base_url)
