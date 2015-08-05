#!/usr/bin/env python
"""
.. module:: attachments
   :synopsis: The attachments class.
"""

import os
import shutil
import uuid

from PyQt4 import QtCore, QtGui, QtWebKit

import misc

class AttachmentsMVC(QtGui.QListView):
    """
    Encapsulates a list view specialized for attachments.
    """
    def __init__(self, parent = None):
        QtGui.QListView.__init__(self, parent)
        self.directory = None
        self.note = None
        self.right_clicked = None

        # Context menu
        self.copyLinkAction = QtGui.QAction(self.tr("Copy Link to Clipboard"), self)
        self.copyLinkAction.triggered.connect(self.handleCopyLink)
        self.deleteAttachmentAction = QtGui.QAction(self.tr("Delete Attachment"), self)
        self.deleteAttachmentAction.triggered.connect(self.handleDeleteAttachment)

        self.popup_menu = QtGui.QMenu(self)
        self.popup_menu.addAction(self.copyLinkAction)

        # Attachments model
        self.attachment_model = QtGui.QStandardItemModel()
        self.setModel(self.attachment_model)

    def addAttachment(self, a_file):
        an_attachment = AttachmentsStandardItem()
        an_attachment.createWithFile(self.directory, a_file)
        self.attachment_model.appendRow(an_attachment)
        self.note.addAttachment(an_attachment.getFullname())
        self.note.saveNote()

    def handleCopyLink(self, boolean):
        clipboard = QtGui.QApplication.clipboard()
        an_attachment = self.attachment_model.itemFromIndex(self.right_clicked)
        clipboard.setText("[" + an_attachment.getFilename() + "](" + an_attachment.getFullname() + ")")

    def handleDeleteAttachment(self, boolean):
        pass

    def mousePressEvent(self, event):
        if (event.button() == QtCore.Qt.RightButton):
            self.right_clicked = self.indexAt(event.pos())
            if (self.right_clicked.row() > -1):
                self.popup_menu.exec_(event.globalPos())
        else:
            QtGui.QListView.mousePressEvent(self, event)
            
    def newNote(self, a_note):
        self.note = a_note
        self.directory = self.note.getNotebook().getDirectory()
        self.attachment_model.clear()
        for fullname in self.note.getAttachments():
            an_attachment = AttachmentsStandardItem()
            an_attachment.createWithFullname(self.directory, fullname)
            self.attachment_model.appendRow(an_attachment)


class AttachmentsStandardItem(QtGui.QStandardItem):
    """
    A single attachment in the attachment listview model.
    """
    def __init__(self):
        QtGui.QStandardItem.__init__(self, "NA")
        self.directory = None  # The notebooks directory.
        self.filename = None   # The attachment file name.
        self.fullname = None   # The attachment file name including the path from self.directory.

    def createWithFullname(self, directory, fullname):
        """
        This is called to load notes that already exist.
        """
        self.directory = directory
        self.filename = os.path.basename(fullname)
        self.fullname = fullname
        self.setText(self.filename)

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

        misc.gitSave(directory,
                     self.fullname,
                     "attachment " + self.filename)

    def getFilename(self):
        return self.filename

    def getFullname(self):
        return self.fullname

    def getUrl(self):
        return self.directory + self.fullname
