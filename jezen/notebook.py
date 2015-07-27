#!/usr/bin/env python
"""
.. module:: notebook
   :synopsis: The NoteBook class.
"""

import os
import uuid

from xml.etree import ElementTree

import misc

class NoteBook(object):
    """
    This class is the interface between notebooks on the disk
    and what is displayed.
    """
    def __init__(self, directory, uuid = None, name = None):
        """
        Load on old notebook (when given a uuid), or create a
        new notebook (when given a name).
        
        Note: The uuid is the directory that the notebook is stored in.
        """
        self.directory = directory

        # Load an old notebook.
        if uuid is not None:
            self.uuid = uuid
            xml = ElementTree.parse(self.directory + self.uuid + "notebook.xml").getroot()
            self.name = xml.find("name").text

            # Load notes.
            
        # Create a new notebook.
        else:
            self.name = name
            self.notes = []
            self.uuid = str(uuid.uuid1())

            os.makedirs(self.directory + self.uuid)

            xml = ElementTree.Element("notebook")
            name_xml = ElementTree.SubElement(xml, "date")
            name_xml.text = self.name

            misc.pSaveXML(self.directory + self.uuid + "/notebook.xml", xml)

            # Create a new git repository for this notebook.

