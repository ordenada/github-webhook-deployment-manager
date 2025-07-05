import os
import telebot
import telebot.types
from typing import Optional

from .log import logger
from .exceptions import MissingEnvironmentVariableException, TelegramException


_TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
try:
    if _TELEGRAM_CHAT_ID is None:
        raise MissingEnvironmentVariableException('TELEGRAM_CHAT_ID')
    TELEGRAM_CHAT_ID = int(_TELEGRAM_CHAT_ID)
except:
    pass

_TELEGRAM_THREAD_ID = os.environ.get('TELEGRAM_THREAD_ID')
try:
    TELEGRAM_THREAD_ID = int(_TELEGRAM_THREAD_ID) \
        if _TELEGRAM_THREAD_ID is not None \
            else None
except:
    pass


def create_bot_client():
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    if TELEGRAM_BOT_TOKEN is None:
        raise MissingEnvironmentVariableException('TELEGRAM_BOT_TOKEN')
    client = telebot.TeleBot(token=TELEGRAM_BOT_TOKEN)
    return client


def send_report(report: str, markdown: Optional[bool] = None, alert: Optional[bool] = None):
    client = create_bot_client()
    
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
        raise TelegramException() from err


def edit_report_message(message_id: int, report: str, markdown: Optional[bool] = None):
    client = create_bot_client()

    try:
        sent_message = client.edit_message_text(
            text=report,
            chat_id=TELEGRAM_CHAT_ID,
            message_id=message_id,
            parse_mode='Markdown' if markdown else None,
        )

        if not isinstance(sent_message, telebot.types.Message):
            raise TelegramException()
        return sent_message.message_id
    except Exception as err:
        logger.error(err)
        raise TelegramException() from err


def delete_report_message(message_id: int):
    client = create_bot_client()
    
    try:
        client.delete_message(
            chat_id=TELEGRAM_CHAT_ID,
            message_id=message_id,
        )
    except Exception as err:
        logger.error(err)
        raise TelegramException() from err
