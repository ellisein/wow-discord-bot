from __future__ import absolute_import

import os
import logging as _logging
from threading import Lock

import config


_logger = None
_logger_level = _logging.INFO

_logger_lock = Lock()

LOG_LEVEL_NAMES = {
    _logging.DEBUG: "DEBUG",
    _logging.INFO: "INFO",
    _logging.WARNING: "WARNING",
    _logging.ERROR: "ERROR",
}


def _get_logger():
    global _logger

    if _logger:
        return _logger

    _logger_lock.acquire()
    try:
        logger = _logging.getLogger("wow-discord-bot")

        logger.setLevel(_logger_level)
        logger_level = config.get("logger_loglevel").upper()
        for k, v in LOG_LEVEL_NAMES.items():
            if v == logger_level:
                logger.setLevel(k)

        formatter = _logging.Formatter("[%(levelname)s] %(message)s")
        streamHandler = _logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)
        if config.get("logger_filelog") == "true":
            fileHandler = _logging.FileHandler("logs.txt")
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)
        
        _logger = logger
        return _logger
    finally:
        _logger_lock.release()

def lname_to_level(lname):
    for l in LOG_LEVEL_NAMES:
        if lname.upper() == LOG_LEVEL_NAMES[l]:
            return l
    return None

def level_to_lname(level):
    if level in LOG_LEVEL_NAMES:
        return LOG_LEVEL_NAMES[level]
    return None

def debug(msg):
    _get_logger().debug(msg)

def info(msg):
    _get_logger().info(msg)

def warning(msg):
    _get_logger().warning(msg)

def error(msg):
    _get_logger().error(msg)
