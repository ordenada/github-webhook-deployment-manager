import os
import telebot
from typing import Optional

from .log import logger


def create_bot_client():
    if os.environ.get('TELEGRAM_BOT_TOKEN') is None:
        logger.error('No set TELEGRAM_BOT_TOKEN')
        return

    TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
    client = telebot.TeleBot(token=TELEGRAM_BOT_TOKEN)
    return client


def send_report(report: str, markdown: Optional[bool] = None, alert: Optional[bool] = None):
    client = create_bot_client()
    if client is None:
        return
    
    TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
    try:
        TELEGRAM_CHAT_ID = int(TELEGRAM_CHAT_ID)
    except:
        pass
    TELEGRAM_THREAD_ID = os.environ.get('TELEGRAM_THREAD_ID')
    
    try:
        client.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=report,
            message_thread_id=TELEGRAM_THREAD_ID,
            parse_mode='Markdown' if markdown else None,
            disable_notification=not alert,
        )
    except Exception as err:
        logger.error(err)
