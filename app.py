# -*- coding: utf-8 -*-
"""
This module is the main entry point for the application.
It imports the necessary dependencies and sets up the environment for the application to run.
"""

from os import environ
import logging
import threading
import flask
from flask import Flask
import telebot

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = telebot.TeleBot(token=environ.get("KEY"))
# Диспетчер


app = Flask(__name__)


@app.route('/')
async def index():
    """
    Render the index.html template for the '/' route.

    :return: The rendered index.html template.
    """
    return flask.render_template('index.html')


if __name__ == '__main__':
    threading.Thread(target=bot.polling(True)).start()
