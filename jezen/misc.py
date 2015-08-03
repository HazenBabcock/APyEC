#!/usr/bin/env python
"""
.. module:: misc
   :synopsis: A collection of miscellaneous functions.
"""

import functools
import os
import subprocess
import uuid

from xml.dom import minidom
from xml.etree import ElementTree

from PyQt4 import QtCore, QtGui

import userinfo_ui as userInfoUi

#
# Decorators
#
def setDirectory(fn):
    @functools.wraps(fn)
    def __wrapper(*args, **kw):
        os.chdir(args[0])
        return(fn(*args, **kw))
    return __wrapper


#
# Functions & Classes
#
def getUserInfo(username, email):
    dialog = UserInfoDialog(username, email)
    dialog.exec_()
    return dialog.getUserInfo()


@setDirectory
def gitGetLastCommit(directory):
    return subprocess.check_output(["git", "log", "-1", "--pretty=%B"])


@setDirectory
def gitGetLog(directory):
    """
    Parses the output of 'git log --name-only --pretty=%H%n%s' and
    returns it as [[commit hash, commit message, file changed], [..]].
    """
    try:
        log_text = subprocess.check_output(["git", "log", "--name-only", "--pretty=%H%n%s"]).splitlines()
    except subprocess.CalledProcessError:
        return []
    
    log = []
    for i in range(len(log_text)/4):
        log.append([log_text[4*i], log_text[4*i+1], log_text[4*i+3]])
    return log

    
@setDirectory
def gitGetVersion(directory, filename, commit_id):
    return subprocess.check_output(["git", "show", commit_id + ":" + filename])

@setDirectory
def gitGetVersionIDs(directory, filename):
    """
    Returns the commit IDs for every version of a file.
    """
    resp = subprocess.check_output(["git", "rev-list", "--all", "--", filename])
    return resp.splitlines()


@setDirectory
def gitInit(directory, name, email):
    subprocess.call(["git", "init"])
    subprocess.call(["git", "config", "user.name", name])
    subprocess.call(["git", "config", "user.email", email])


@setDirectory
def gitSave(directory, filename, commit):
    subprocess.call(["git", "add", filename])
    subprocess.call(["git", "commit", "-m", commit])

    
def pSaveXML(filename, xml):
    """
    Save XML to a file in a 'pretty' format.
    """
    
    rough_string = ElementTree.tostring(xml, 'utf-8')
    reparsed = minidom.parseString(rough_string)
        
    with open(filename, "w") as fp:
        fp.write(reparsed.toprettyxml(indent="  ", encoding = "ISO-8859-1"))


class UserInfoDialog(QtGui.QDialog):
    """
    Dialog for getting (or changing) the username and email address used by git.
    """
    def __init__(self, username, email, parent = None):
        QtGui.QDialog.__init__(self, parent)

        self.ui = userInfoUi.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("(Git) User Information")

        self.ui.usernameLineEdit.setText(username)
        self.ui.emailLineEdit.setText(email)

    def closeEvent(self, event):
        if (len(self.ui.usernameLineEdit.text()) == 0) or (len(self.ui.emailLineEdit.text()) == 0):
            event.ignore()

    def getUserInfo(self):
        return [self.ui.usernameLineEdit.text(),
                self.ui.emailLineEdit.text()]
