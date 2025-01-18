import os
import telebot
from typing import Optional

from .log import logger


def create_bot_client():
    if os.environ.get('TELEGRAM_BOT_TOKEN') is None:
        logger.error('No set TELEGRAM_BOT_TOKEN')
        return

    token = os.environ['TELEGRAM_BOT_TOKEN']
    client = telebot.TeleBot(token=token)
    return client


def send_report(report: str, alert: bool[bool] = None):
    client = create_bot_client()
    if client is None:
        return
    
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    try:
        chat_id = int(chat_id)
    except:
        pass
    thread_id = os.environ.get('TELEGRAM_THREAD_ID')
    
    try:
        client.send_message(
            chat_id=chat_id,
            text=report,
            message_thread_id=thread_id,
            disable_notification=not alert,
        )
    except Exception as err:
        logger.error(err)
