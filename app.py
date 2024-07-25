# -*- coding: utf-8 -*-
"""
This module is the main entry point for the application.
It imports the necessary dependencies and sets up the environment for the application to run.
"""

from logging import INFO
from threading import Thread

import flask
import telebot
from black import Any

# pylint: disable=import-error
from log_handle import logger as log
from token_handler import result as bot

logger = telebot.logger
telebot.logger.setLevel(INFO)

Thread(target=bot.infinity_polling, daemon=True).start()

log.info("Telebot started!")

app = flask.Flask(__name__)


@app.route("/")
async def index() -> str:
    """
    Render the index.html template for the '/' route.

    :rtype: str
    :return: The rendered index.html template.
    """

    return flask.render_template("index.html")


@app.route("/api/message/send", methods=["POST"])
async def send_message() -> flask.Response | tuple[Any, int]:
    """
    Send a message to the specified chat ID.

    :returns: A JSON response indicating whether the message was sent successfully.
    """

    try:
        request_json = flask.request.json
        if request_json is None:
            return flask.jsonify({"success": False, "error": "Invalid JSON"}), 400

        chat_id = request_json.get("chat_id")
        message = request_json.get("message")

        if chat_id is None or message is None:
            return (
                flask.jsonify({"success": False, "error": "Missing chat_id or message"}),
                400,
            )
        response = bot.send_message(chat_id, message)
    except Exception as e:  # pylint: disable=broad-except
        return flask.jsonify({"success": False, "error": str(e)})
    return flask.jsonify(response), 201
