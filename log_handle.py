#!/usr/bin/env python

"""
This module contains the logger setup and log levels for the application.
"""
# -*- coding: utf-8 -*-
from sys import stdout
from loguru import logger


class Level:  # pylint: disable=too-few-public-methods
    """
    A class that defines the different log levels for the logger.

    This class defines the log levels that can be used with the logger. Each log level
    is associated with a string constant and a color constant. The string constants
    are used to identify the log level in the log message. The color constants are used
    to color the log message in the terminal.

    The log levels are:
    - TRACE: "TRACE"
    - DEBUG: "DEBUG"
    - INFO: "INFO"
    - SUCCESS: "SUCCESS"
    - WARNING: "WARNING"
    - ERROR: "ERROR"

    The associated colors are:
    - TRACE: "<dim><white>"
    - DEBUG: "<blue>"
    - INFO: "<green>"
    - SUCCESS: "<green>"
    - WARNING: "<yellow>"
    - ERROR: "<red>"
    """

    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"

    TRACE_COLOR = "<dim><white>"
    DEBUG_COLOR = "<blue>"
    INFO_COLOR = "<green>"
    SUCCESS_COLOR = "<green>"
    WARNING_COLOR = "<yellow>"
    ERROR_COLOR = "<red>"

    TRACE_ICON = "🔵 T"
    DEBUG_ICON = "🔵 D"
    INFO_ICON = "🟢 I"
    SUCCESS_ICON = "🟢 S"
    WARNING_ICON = "🟡 W"
    ERROR_ICON = "🔴 E"


# removing default logger, setting up levels and adding new loggers
logger.remove()
logger.level(Level.TRACE, color=Level.TRACE_COLOR, icon=Level.TRACE_ICON)
logger.level(Level.DEBUG, color=Level.DEBUG_COLOR, icon=Level.DEBUG_ICON)
logger.level(Level.INFO, color=Level.INFO_COLOR, icon=Level.INFO_ICON)
logger.level(Level.SUCCESS, color=Level.SUCCESS_COLOR, icon=Level.SUCCESS_ICON)
logger.level(Level.WARNING, color=Level.WARNING_COLOR, icon=Level.WARNING_ICON)
logger.level(Level.ERROR, color=Level.ERROR_COLOR, icon=Level.ERROR_ICON)

# setting up stdout handler
logger.add(
    stdout,
    format="<white>{time:HH:mm:ss}</white> |"
    " <level>[{level.icon}]</level> |"
    " <level>{message}</level>",
    colorize=True,
    level=Level.INFO,
)

# setting up file handler
logger.add(
    "logs/{time:YYYY-MM-DD}.log",
    format="{time:HH:mm:ss} | {level} | {message}",
    level=Level.TRACE,
    rotation="00:00",
    compression="zip",
    retention="7 days",
    colorize=False,
)
