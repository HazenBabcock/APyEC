#!/usr/bin/env python

import diffMatchPatch
import os

from xml.dom import minidom
from xml.etree import ElementTree

class NoteHandler(object):
    """
    This class is the interface between the notes on the disk and
    what is displayed. It takes care of loading and saving different
    versions using our XML schema.
    """
    def __init__(self, filename):
        self.filename = filename

        # Load the note if it exists.
        if os.path.exists(filename):
            self.xml = ElementTree.parse(note_filename).getroot()

        # Otherwise create an empty note xml structure.
        self.xml = ElementTree.Element("note")

    def loadNote(self, version):
        for note in self.xml:
            for field in note:
                if (field.tag == "text"):
                    return field.text
        return ""

    def saveNote(self, note_text):

        # Update XML.
        note_xml = ElementTree.SubElement(self.xml, "note")
        date_xml = ElementTree.SubElement(note_xml, "date")
        text_xml = ElementTree.SubElement(note_xml, "text")
        text_xml.text = note_text
        version_xml = ElementTree.SubElement(note_xml, "version")

        # Save to disk.
        rough_string = ElementTree.tostring(self.xml, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        
        with open(self.filename, "w") as fp:
            fp.write(reparsed.toprettyxml(indent="  ", encoding = "ISO-8859-1"))

