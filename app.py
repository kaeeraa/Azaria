# -*- coding: utf-8 -*-
"""
This module is the main entry point for the application.
It imports the necessary dependencies and sets up the environment for the application to run.
"""

from logging import INFO

from os import environ
from threading import Thread

import flask
import telebot

# pylint: disable=import-error
from log_handle import logger as log

# from config_handler import result as config
# from version import __version__

bot = telebot.TeleBot(token=environ.get("KEY"))
logger = telebot.logger
telebot.logger.setLevel(INFO)

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


Thread(target=bot.infinity_polling).start()
