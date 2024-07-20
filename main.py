#!/usr/bin/env python

"""
This module contains the main entry point of the application.
It imports necessary modules and sets up the environment.
"""

# -*- coding: utf-8 -*-

__VERSION__ = "0.0.1"

import sys

import shutil
from sys import stdout
import tomllib
from loguru import logger

import app  # pylint: disable=import-error


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
logger.add(stdout,
           format="<white>{time:HH:mm:ss}</white> |"
                  " <level>[{level.icon}]</level> |"
                  " <level>{message}</level>",
           colorize=True, level=Level.INFO)

# setting up file handler
logger.add("logs/{time:YYYY-MM-DD}.log", format="{time:HH:mm:ss} | {level} | {message}",
           level=Level.TRACE, rotation="00:00", compression="zip", retention="7 days",
           colorize=False)

logger.trace("Logging started")


def caught(exception: Exception, critical: bool = False) -> None:
    """
    This function handles exceptions based on the critical flag.

    :param exception: The exception that was caught.
    :param critical: A flag indicating if the exception is critical.

    :return: None
    """
    if critical:
        logger.error("We have caught an exception: " + str(exception))
        input("Press any key to exit...")
        sys.exit(1)
    else:
        logger.error("We have caught an exception: " + str(exception))


def bad_config() -> None:
    """
    A function that handles the configuration setup, if the config is invalid or corrupted.
    Prompts the user to create a new config file, renames the existing one if it exists,
    and provides instructions on editing the config file.

    :return: None
    """

    if input("Would you like to create a new config file?"
             " If your config file already exists, it will be renamed to "
             "config.toml.bak (y/n) ") == "y":
        try:
            shutil.move("user/config.toml", "./user/config.toml.bak")
            shutil.copyfile("resources/default_config.toml", "user/config.toml")
        except Exception as e:  # pylint: disable=broad-except
            caught(e, True)
        logger.success("Created new default config file,"
                       " old config file renamed to config.toml.bak")
        logger.info("Please edit config.toml to your liking")
    else:
        logger.error("Exiting...")
        sys.exit()


# loading config
with open("user/config.toml", 'rb') as stream:
    options: list = ['token', 'explicit-control']

    try:
        config: dict = tomllib.load(stream)
    except tomllib.TOMLDecodeError as exc:
        caught(exc)
        bad_config()

    if config is None:
        caught("Config file is empty")
        bad_config()

    if 'config-version' not in list(config.keys()):
        caught("Config file is missing config-version")
        bad_config()

    if config['config-version'] != int(__VERSION__.replace(".", "")):
        caught("Config version mismatch")
        bad_config()

    try:
        if not isinstance(config['token'], str) or \
                not isinstance(config['explicit-control']['enabled'], bool) or \
                not isinstance(config['explicit-control']['type'], str):
            caught("Config file is invalid")
            bad_config()
    except KeyError as exc:
        caught("Config file is missing keys")
        bad_config()

    logger.info("Config loaded")

if config['explicit-control']['enabled']:
    logger.info("Explicit control enabled")
    match config['explicit-control']['type'].lower():
        case "web":
            logger.info("Running in web mode")
            panelType: str = "web"
        case "cli":
            logger.info("Running in cli (terminal) mode")
            panelType: str = "cli"
        case _:
            logger.warning("Invalid explicit control mode, using cli (terminal) mode")
            logger.info("Running in cli (terminal) mode")
            panelType: str = "cli"
else:
    logger.info("Explicit control disabled")
    while 1:
        panelType = input("Enter 'web' for web mode, 'cli' for cli (terminal) mode: ").lower()
        if panelType in ["web", "cli"]:
            break
        logger.warning("Invalid input, please enter 'web' or 'cli'")
    logger.info(f"Running in {panelType} mode")

    app.app.run(use_reloader=False, host="0.0.0.0", port=7171, threaded=True)

    logger.info("More is not implemented yet (indev)")

    # raise NotImplementedError
