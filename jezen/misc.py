#!/usr/bin/env python
"""
.. module:: misc
   :synopsis: A collection of miscellaneous functions.
"""

import os
import uuid

from xml.dom import minidom
from xml.etree import ElementTree

def pSaveXML(filename, xml):
    """
    Save XML to a file in a 'pretty' format.
    """
    
    rough_string = ElementTree.tostring(xml, 'utf-8')
    reparsed = minidom.parseString(rough_string)
        
    with open(filename, "w") as fp:
        fp.write(reparsed.toprettyxml(indent="  ", encoding = "ISO-8859-1"))
