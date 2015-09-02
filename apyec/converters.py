#!/usr/bin/env python
"""
.. module:: converters
   :synopsis: Converters for handling various types of content.
"""

import docutils
import docutils.core
import markdown
import os

content_types = ["markdown", "ReST"]

# Content converters.
def convertMDtoHTML(markdown_text):
    return markdown.markdown(markdown_text)

def convertReSTtoHTML(rest_text):
    return docutils.core.publish_string(rest_text, writer_name = 'html')

def getHTMLConverter(content_type):
    if (content_type == "markdown"):
        return convertMDtoHTML
    elif (content_type == "ReST"):
        return convertReSTtoHTML
    else:
        raise ContentTypeException(content_type)

def getLinkConverter(content_type):
    if (content_type == "markdown"):
        return linkConverterMD
    elif (content_type == "ReST"):
        return linkConverterReST
    else:
        raise ContentTypeException(content_type)    

def linkConverterMD(link_name, link_url, is_image):
    extension = os.path.splitext(link_name)[1]
    if is_image:
        return "![" + link_name + "](" + link_url + ")"
    else:
        return "[" + link_name + "](" + link_url + ")"

def linkConverterReST(link_name, link_url, is_image):
    extension = os.path.splitext(link_name)[1]
    if is_image:
        return ".. figure:: " + link_url
    else:
        return "`" + link_name + " <" + link_url + ">`_"

class ContentTypeException(Exception):
    def __init__(self, message):
        message = "Error no converter exists for " + message
        Exception.__init__(self, message)

        
