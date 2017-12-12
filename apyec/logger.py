#!/usr/bin/env python
"""
.. module:: logger
   :synopsis: Handles logging (for debugging).
"""

import functools
import logging
import logging.handlers

from PyQt5 import QtCore

a_logger = False

def logFn(fn):
    """
    Wraps a function or method call to save logging information.
    """
    global a_logger
    @functools.wraps(fn)
    def __wrapper(*args, **kw):
        if a_logger:
            a_logger.info(fn.__module__ + "." + fn.__name__ + " started")
            for i, arg in enumerate(args):
                a_logger.info("   " + str(i) + " " + str(arg))
        temp = fn(*args, **kw)
        if a_logger:
            a_logger.info(fn.__module__ + "." + fn.__name__ + " ended")
        return temp
    return __wrapper

def startLogging(directory):
    global a_logger

    settings = QtCore.QSettings("apyec", "apyec")
    index = int(settings.value("logging_file_index", 1))
    new_index = index + 1
    if (new_index > 100):
        new_index = 1
    settings.setValue("logging_file_index", new_index)

    # Initialize logger.
    a_logger = logging.getLogger("apyec")
    a_logger.setLevel(logging.DEBUG)

    # Create formatter.
    rt_formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')

    # Rotating file handle for saving output.
    log_filename = directory + "apyec_log" + str(index) + ".out"
    try:
        rf_handler = logging.handlers.RotatingFileHandler(log_filename,
                                                          maxBytes = 200000,
                                                          backupCount = 5)
    except IOError:
        print("Logging Error! Could not open", log_filename)
        print("  Logging is disabled.")
        a_logger = False

    if a_logger:
        rf_handler.setFormatter(rt_formatter)
        a_logger.addHandler(rf_handler)
