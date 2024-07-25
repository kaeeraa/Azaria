#!/usr/bin/env python

"""
This module contains the tests for the application.

The tests are written using the pytest framework.
"""

# -*- coding: utf-8 -*-

from typing import Any
from json import dumps
from sys import argv
from os import environ

from telebot import TeleBot
from telebot.types import Message
from dotenv import get_key

# pylint: disable=import-error
from config_handler import init
from config_handler import result as config
from log_handle import logger as log

if argv and argv[1].startswith("-t "):
    bot = TeleBot(token=argv[1][3:])
    log.info("Using command line argument KEY")
elif environ.get("KEY"):
    bot = TeleBot(token=environ.get("KEY"))
    log.info("Using environment variable KEY")
elif get_key(".env", "KEY"):
    bot = TeleBot(token=get_key(".env", "KEY"))
    log.info("Using .env file KEY")
else:
    bot = TeleBot(token=config["token"])
    log.info("Using config file KEY")


def test_send_message():
    """Test the send_message function."""

    def send_message(chat_id: str = None, message: str = None) -> tuple[Any, int]:
        """
        Send a message to the specified chat ID.

        :returns: A JSON response indicating whether the message was sent successfully.
        """
        try:
            response: Message = bot.send_message(chat_id, message)
        except Exception as e:  # pylint: disable=broad-except
            return dumps({'success': False, 'error': str(e)}), 500
        return dumps(response.json), 201

    request: tuple[Any, int] = send_message(1807149159, 'test message')
    assert request[1] == 201


def test_init():
    """Test the index function."""

    assert init() is not None
