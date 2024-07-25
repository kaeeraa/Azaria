# -*- coding: utf-8 -*-
"""
This module is the main entry point for the application.
It imports the necessary dependencies and sets up the environment for the application to run.
"""

from logging import INFO
from os import environ
from sys import argv

import flask
import telebot
from telebot import TeleBot
from dotenv import get_key

# pylint: disable=import-error
from log_handle import logger as log
from config_handler import result as config

if argv and len(argv) >= 3 and argv[1] == "--token":
    bot = TeleBot(token=argv[2])
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

# from version import __version__


logger = telebot.logger
telebot.logger.setLevel(INFO)

bot.infinity_polling()

log.info("Telebot started!")

app = flask.Flask(__name__)


@app.route('/')
async def index():
    """
    Render the index.html template for the '/' route.

    :return: The rendered index.html template.
    """

    return flask.render_template('index.html')


@app.route('/api/message/send', methods=['POST'])
async def send_message() -> flask.Response:
    """
    Send a message to the specified chat ID.

    :returns: A JSON response indicating whether the message was sent successfully.
    """

    try:
        chat_id = flask.request.json['chat_id']
        message = flask.request.json['message']
        response = bot.send_message(chat_id, message)
    except Exception as e:  # pylint: disable=broad-except
        return flask.jsonify({'success': False, 'error': str(e)})
    return flask.jsonify(response.json), 201
