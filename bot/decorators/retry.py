from time import sleep

from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import RetryAfter


def retry_after(callback):
    '''Aguarda o tempo necessário quando ocorre um erro RetryAfter.
    '''
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            return await callback(update, context)
        except RetryAfter as error:
            sleep(error.retry_after + 1)
            return await callback(update, context)

    return wrapper
