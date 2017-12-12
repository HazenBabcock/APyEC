#!/usr/bin/env python
"""
.. module:: noteTextEdit
   :synopsis: A QTextEdit specialized for editting notes.
"""

from PyQt5 import QtWidgets


class NoteTextEdit(QtWidgets.QTextEdit):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.note_content = None
                 
    def insertFromMimeData(self, mimedata):
        # Check if this a link to a note that the user is trying to paste.
        if mimedata.hasText():
            text = str(mimedata.text())
            if (text[:11] == "<note_link>") and (text[-12:] == "</note_link>"):
                data = text.split("<split>")
                if (len(data) == 4):
                    self.insertPlainText(self.note_content.formatLink(data[1], "apyec:/" + data[2]))
                    return
        super().insertFromMimeData(mimedata)
    
    def setNoteContent(self, note_content):
        self.note_content = note_content
