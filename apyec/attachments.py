#!/usr/bin/env python
"""
.. module:: attachments
   :synopsis: The attachments class.
"""

import imghdr
import os
import shutil
import uuid

from PyQt5 import QtCore, QtGui, QtWidgets

import logger
import misc

class AttachmentsMVC(QtWidgets.QListView):
    """
    Encapsulates a list view specialized for attachments.
    """
    @logger.logFn    
    def __init__(self, parent = None):
        super().__init__(parent)

        self.directory = None      # This is the directory associated with the notebook.
        self.note = None
        self.note_content = None
        self.right_clicked = None
        self.settings = QtCore.QSettings("apyec", "apyec")

        # This is the directory where an attachment was most recently saved to.
        self.saveas_directory = str(self.settings.value("saveas_directory", "."))

        # Drag and drop
        self.setAcceptDrops(True)
        
        # Context menu
        self.copyLinkAction = QtWidgets.QAction(self.tr("Copy Link to Clipboard"), self)
        self.copyLinkAction.triggered.connect(self.handleCopyLink)
        self.deleteAttachmentAction = QtWidgets.QAction(self.tr("Delete Attachment"), self)
        self.deleteAttachmentAction.triggered.connect(self.handleDeleteAttachment)
        self.saveAsAction = QtWidgets.QAction(self.tr("Save Attachment as"), self)
        self.saveAsAction.triggered.connect(self.handleSaveAs)

        self.popup_menu = QtWidgets.QMenu(self)
        self.popup_menu.addAction(self.copyLinkAction)
        self.popup_menu.addAction(self.deleteAttachmentAction)
        self.popup_menu.addAction(self.saveAsAction)

        # Attachments model
        self.attachment_model = QtWidgets.QStandardItemModel()
        self.setModel(self.attachment_model)

    @logger.logFn        
    def addAttachment(self, a_file):
        an_attachment = AttachmentsStandardItem()
        an_attachment.createWithFile(self.directory, a_file)
        self.attachment_model.appendRow(an_attachment)
        self.note_content.addAttachment(an_attachment.getFullname())
        self.note.saveNote(self.note_content)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        self.dragEnterEvent(event)
        
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            for url in event.mimeData().urls():
                print(str(url.toLocalFile()))
                self.addAttachment(str(url.toLocalFile()))
        else:
            event.ignore()
        
    @logger.logFn        
    def handleCopyLink(self, boolean):
        clipboard = QtWidgets.QApplication.clipboard()
        an_attachment = self.attachment_model.itemFromIndex(self.right_clicked)
        clipboard.setText(self.note_content.formatLink(an_attachment.getFilename(),
                                                       an_attachment.getFullname(),
                                                       an_attachment.isImage()))

    @logger.logFn        
    def handleDeleteAttachment(self, boolean):
        an_attachment = self.attachment_model.itemFromIndex(self.right_clicked)
        self.note_content.removeAttachment(an_attachment.getFullname())
        self.note.saveNote(self.note_content)
        self.attachment_model.removeRow(self.right_clicked.row())

    @logger.logFn
    def handleSaveAs(self, boolean):
        an_attachment = self.attachment_model.itemFromIndex(self.right_clicked)
        saveas_filename = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                "Save As",
                                                                self.saveas_directory + "/" + an_attachment.getFilename(),
                                                                "*")
        if saveas_filename:
            saveas_filename = str(saveas_filename)
            self.saveas_directory = os.path.dirname(saveas_filename)
            self.settings.setValue("saveas_directory", self.saveas_directory)
            an_attachment.saveACopy(saveas_filename)
        
    @logger.logFn    
    def mousePressEvent(self, event):
        if (event.button() == QtCore.Qt.RightButton):
            self.right_clicked = self.indexAt(event.pos())
            if (self.right_clicked.row() > -1):
                self.popup_menu.exec_(event.globalPos())
        else:
            super().mousePressEvent(self, event)

    @logger.logFn
    def newNote(self, a_note, note_content):
        self.note = a_note
        self.note_content = note_content
        self.directory = self.note.getNotebook().getDirectory()
        self.attachment_model.clear()
        for fullname in self.note_content.getAttachments():
            an_attachment = AttachmentsStandardItem()
            an_attachment.createWithFullname(self.directory, fullname)
            self.attachment_model.appendRow(an_attachment)


class AttachmentsStandardItem(QtGui.QStandardItem):
    """
    A single attachment in the attachment listview model.
    """
    @logger.logFn    
    def __init__(self):
        super().__init__("NA")
        
        self.setEditable(False)
        self.directory = None  # The notebooks directory.
        self.filename = None   # The attachment file name.
        self.fullname = None   # The attachment file name including the path from self.directory.
        self.is_image = False

    @logger.logFn        
    def createWithFullname(self, directory, fullname):
        """
        This is called to load attachments that already exist.
        """
        self.directory = directory
        self.filename = os.path.basename(fullname)
        self.fullname = fullname
        self.setText(self.filename)
        self.imageCheck()

    @logger.logFn        
    def createWithFile(self, directory, a_file):
        """
        This is called to create a new attachment from a file.
        """
        self.directory = directory
        self.filename = os.path.basename(a_file)
        self.fullname = "attach_" + str(uuid.uuid1()) + "/"
        os.makedirs(self.directory + self.fullname)
        self.fullname += self.filename
        shutil.copy(a_file, self.directory + self.fullname)
        self.setText(self.filename)

        misc.gitAddCommit(directory,
                          self.fullname,
                          "attachment " + self.filename)

        self.imageCheck()
        
    @logger.logFn        
    def getFilename(self):
        return self.filename

    @logger.logFn    
    def getFullname(self):
        return self.fullname

    @logger.logFn    
    def getUrl(self):
        return self.directory + self.fullname

    @logger.logFn
    def imageCheck(self):
        if imghdr.what(self.directory + self.fullname) is not None:
            self.is_image = True
            
    @logger.logFn
    def isImage(self):
        return self.is_image

    @logger.logFn
    def saveACopy(self, filename):
        shutil.copy(self.directory + self.fullname, filename)

