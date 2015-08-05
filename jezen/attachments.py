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

        self.attach_model = QtGui.QStandardItemModel()
        self.setModel(self.attach_model)

    def addAttachment(self, a_file):
        an_attachment = AttachmentsStandardItem()
        an_attachment.createWithFile(self.directory, a_file)
        self.attach_model.appendRow(an_attachment)
        self.note.addAttachment(an_attachment.getFullname())
        self.note.saveNote()

    def newNote(self, a_note):
        self.note = a_note
        self.directory = self.note.getNotebook().getDirectory()
        self.attach_model.clear()
        for fullname in self.note.getAttachments():
            an_attachment = AttachmentsStandardItem()
            an_attachment.createWithFullname(self.directory, fullname)
            self.attach_model.appendRow(an_attachment)


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

    def getFullname(self):
        return self.fullname

