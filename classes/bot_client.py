import os
import telebot
from typing import Optional

from .log import logger


TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
try:
    TELEGRAM_CHAT_ID = int(TELEGRAM_CHAT_ID)
except:
    pass
TELEGRAM_THREAD_ID = os.environ.get('TELEGRAM_THREAD_ID')


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
    
    try:
        sent_message = client.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=report,
            message_thread_id=TELEGRAM_THREAD_ID,
            parse_mode='Markdown' if markdown else None,
            disable_notification=not alert,
        )
        return sent_message.message_id
    except Exception as err:
        logger.error(err)
        raise err


def edit_report_message(message_id: int, report: str, markdown: Optional[bool] = None):
    client = create_bot_client()
    if client is None:
        return

    try:
        sent_message = client.edit_message_text(
            text=report,
            chat_id=TELEGRAM_CHAT_ID,
            message_id=message_id,
            parse_mode='Markdown' if markdown else None,
        )
        return sent_message.message_id
    except Exception as err:
        logger.error(err)


def delete_report_message(message_id: int):
    client = create_bot_client()
    if client is None:
        return
    
    try:
        client.delete_message(
            chat_id=TELEGRAM_CHAT_ID,
            message_id=message_id,
        )
    except Exception as err:
        logger.error(err)
