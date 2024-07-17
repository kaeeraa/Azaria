#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shutil

from loguru import logger
from sys import stdout
import yaml
from sys import exit


class Level:
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

    TRACE_ICON = "🔵"
    DEBUG_ICON = "🔵"
    INFO_ICON = "🟢"
    SUCCESS_ICON = "🟢"
    WARNING_ICON = "🟡"
    ERROR_ICON = "🔴"


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
           format="<white>{time:HH:mm:ss}</white> | <level>[{level.icon}]</level> | <level>{message}</level>",
           colorize=True, level="INFO")

# setting up file handler
logger.add("logs/{time:YYYY-MM-DD}.log", format="{time:HH:mm:ss} | {level} | {message}",
           level="TRACE", rotation="00:00", compression="zip", retention="7 days", colorize=False)

logger.trace("Logging started")


def caught(exception: Exception, critical: bool = False):
    if critical:
        logger.error("We have caught an exception: " + str(exception))
        input("Press any key to exit...")
    else:
        logger.error("We have caught an exception: " + str(exception))


def bad_config():
    if input("Would you like to create a new config file? If your config file already exists, it will be renamed to "
             "config.yaml.bak (y/n) ") == "y":
        try:
            shutil.move("./user/config.yaml", "./user/config.yaml.bak")
            shutil.copyfile("./resources/default_config.yaml", "./user/config.yaml")
        except Exception as e:
            logger.exception(e)
        logger.success("Created new default config file, old config file renamed to config.yaml.bak")
        logger.info("Please edit config.yaml to your liking")
        input("Press any key to exit...")
        exit()
    else:
        logger.error("Exiting...")
        exit()


logger.catch(onerror=lambda e: caught(e))

# loading config
with open("./user/config.yaml") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        logger.exception(exc)
        bad_config()

    if config is None:
        bad_config()

    logger.info("Config loaded")
