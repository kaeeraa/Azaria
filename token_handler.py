#!/usr/bin/env python
"""
This module is responsible for handling the Telegram bot token.

It imports necessary modules and sets up the environment for the application to run.
The bot token is fetched from the configuration file and passed to the TeleBot object.
The bot token can be passed as a command line argument or as an environment variable.
If none of these options are provided, the bot token will be fetched from the configuration file.
"""
from os import environ

# -*- coding: utf-8 -*-
from sys import argv
from dotenv import get_key
from telebot import TeleBot

# pylint: disable=import-error
from config_handler import result as config
from log_handle import logger as log

log.info("Token handler started")


def export_token() -> TeleBot:
    """
    This function returns a TeleBot object with the token from the config file.

    :return: A TeleBot object with the token from the config file.
    :rtype: TeleBot
    :usage: bot = exportToken()
    """
    if argv and len(argv) >= 3 and argv[1] == "--token":
        log.info("Using command line argument KEY")
        return TeleBot(token=argv[2])
    if environ.get("KEY"):
        log.info("Using environment variable KEY")
        return TeleBot(token=environ.get("KEY"))
    if get_key(".env", "KEY"):
        log.info("Using .env file KEY")
        return TeleBot(token=get_key(".env", "KEY"))
    # If no token is provided, the bot will take the token from the config file.
    log.info("Using config file KEY")
    return TeleBot(token=config["token"])


log.success("Token handler finished")
result: TeleBot = export_token()
