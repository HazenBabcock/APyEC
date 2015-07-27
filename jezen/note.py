#!/usr/bin/env python
"""
.. module:: note
   :synopsis: The Note class.
"""

import os
import uuid

from xml.dom import minidom
from xml.etree import ElementTree

import misc

class Note(object):
    """
    This class is the interface between the notes on the disk and
    what is displayed. It takes care of loading and saving different
    versions using our XML schema.
    """
    def __init__(self, directory, uuid = None, name = None):
        """
        Load on old note (when given a uuid), or create a
        new note (when given a name).
        
        Note: The uuid is the actual name of the note file on the disk.
        """
        self.directory = directory

        # Load an old note.
        if uuid is not None:
            self.uuid = uuid
            xml = ElementTree.parse(self.directory + self.uuid).getroot()
            self.markdown = xml.find("markdown").text
            self.name = xml.find("name").text

        # Create a new note.
        else:
            self.markdown = ""
            self.name = name
            self.uuid = str(uuid.uuid1())

    def saveNote(self):

        # Update XML.
        xml = ElementTree.Element("note")
        
        name_xml = ElementTree.SubElement(xml, "date")
        name_xml.text = self.name
        
        markdown_xml = ElementTree.SubElement(xml, "text")
        markdown_xml.text = self.markdown

        misc.pSaveXML(self.directory + self.uuid, xml)

        # Use git to check if this file is different from before
        # and create a commit if it is.

