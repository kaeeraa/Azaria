#!/usr/bin/env python

"""
This module contains the tests for the application.

The tests are written using the pytest framework.
"""

# -*- coding: utf-8 -*-

from typing import Any
from json import dumps

from telebot.types import Message

# pylint: disable=import-error
from config_handler import init
from token_handler import result as bot


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
