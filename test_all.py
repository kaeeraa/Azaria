#!/usr/bin/env python

"""
This module contains the tests for the application.

The tests are written using the pytest framework.
"""

# -*- coding: utf-8 -*-

from json import dumps

from black import Any, Optional
from telebot.types import Message

# pylint: disable=import-error
from config_handler import init
from token_handler import result as bot


def test_send_message():  # type: ignore
    """Test the send_message function."""

    def send_message(
        chat_id: Optional[str] = None, message: Optional[str] = None
    ) -> tuple[Any, int]:
        """
        Send a message to the specified chat ID.

        :type message: object
        :type chat_id: object

        :rtype: object
        :returns: A JSON response indicating whether the message was sent successfully.
        """
        try:
            response: Message = bot.send_message(chat_id, message)
        except Exception as e:  # pylint: disable=broad-except
            return dumps({"success": False, "error": str(e)}), 500
        return dumps(response.json), 201

    request = send_message("1807149159", "test message")

    assert isinstance(request, tuple) and len(request) == 2
    assert request[1] == 201


def test_init():  # type: ignore
    """Test the index function."""

    assert init() is not None
