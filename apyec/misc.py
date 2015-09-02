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

import logger

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
@logger.logFn
def getUserInfo(username, email):
    dialog = UserInfoDialog(username, email)
    dialog.exec_()
    return dialog.getUserInfo()


@logger.logFn
@setDirectory
def gitAddCommit(directory, files, commit):
    if isinstance(files, list):
        for f in files:
            subprocess.call(["git", "add", f])
    else:
        subprocess.call(["git", "add", files])        
    subprocess.call(["git", "commit", "-m", commit])
    
    
@logger.logFn
@setDirectory
def gitGetLastCommit(directory):
    return subprocess.check_output(["git", "log", "-1", "--pretty=%B"])


@logger.logFn
@setDirectory
def gitGetLastCommitId(directory):
    """
    Returns the SHA-1 id of the last commit.
    """
    return subprocess.check_output(["git", "log", "-1", "--pretty=%H"]).strip()


@logger.logFn
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


@logger.logFn
@setDirectory
def gitGetVersion(directory, filename, commit_id):
    return subprocess.check_output(["git", "show", commit_id + ":" + filename])


@logger.logFn
@setDirectory
def gitGetVersionIDs(directory, filename):
    """
    Returns the commit IDs for every version of a file.
    """
    resp = subprocess.check_output(["git", "rev-list", "--all", "--", filename])
    return resp.splitlines()


@logger.logFn
@setDirectory
def gitHasRemote(directory):
    """
    Returns true if a remote repository has been configured for a notebook.
    """
    resp = subprocess.check_output(["git", "remote", "-v"])
    if (len(resp) > 0):
        return True
    else:
        return False


@logger.logFn
@setDirectory
def gitHasUnpushed(directory):
    """
    Returns true if the local notebook has changes that have not been
    pushed to the remote notebook.

    Note this assumes that the local branch is master and upstream is origin/master.
    """
    if not gitHasRemote(directory):
        return True
    
    resp = subprocess.check_output(["git", "cherry", "-v", "origin/master"])
    if (len(resp) > 0):
        return True
    else:
        return False

    
@logger.logFn
@setDirectory
def gitInit(directory, name, email):
    subprocess.call(["git", "init"])
    subprocess.call(["git", "config", "user.name", name])
    subprocess.call(["git", "config", "user.email", email])


@logger.logFn
@setDirectory
def gitRemove(directory, filename, commit):
    subprocess.call(["git", "rm", filename])
    subprocess.call(["git", "commit", "-m", commit])
    

@logger.logFn    
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
    @logger.logFn
    def __init__(self, username, email, parent = None):
        QtGui.QDialog.__init__(self, parent)

        self.ui = userInfoUi.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("(Git) User Information")

        self.ui.usernameLineEdit.setText(username)
        self.ui.emailLineEdit.setText(email)

    @logger.logFn
    def closeEvent(self, event):
        if (len(self.ui.usernameLineEdit.text()) == 0) or (len(self.ui.emailLineEdit.text()) == 0):
            event.ignore()

    @logger.logFn            
    def getUserInfo(self):
        return [self.ui.usernameLineEdit.text(),
                self.ui.emailLineEdit.text()]
