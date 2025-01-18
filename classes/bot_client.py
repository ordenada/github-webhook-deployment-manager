import os
import telebot

from .log import logger


def create_bot_client():
    if os.environ.get('TELEGRAM_BOT_TOKEN') is None:
        logger.error('No set TELEGRAM_BOT_TOKEN')
        return

    token = os.environ['TELEGRAM_BOT_TOKEN']
    client = telebot.TeleBot(token=token)
    return client
