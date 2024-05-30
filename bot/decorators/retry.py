from time import sleep

from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import RetryAfter

from bot.functions.chat import message_edit_reply_markup


def retry_after(callback):
    '''Aguarda o tempo necessário quando ocorre um erro RetryAfter.
    '''
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.effective_message
        query = update.callback_query
        if query:
            old_reply_markup = query.message.reply_markup

        try:
            return await callback(update, context)
        except RetryAfter as error:
            sleep_time = error.retry_after + 10
            print(f'RetryAfter: Retrying in {sleep_time} seconds...')
            sleep(sleep_time)

            query = update.callback_query
            if query:
                new_reply_markup = query.message.reply_markup
                if old_reply_markup and old_reply_markup != new_reply_markup:
                    await message_edit_reply_markup(
                        function_caller='RETRY.RETRY_AFTER()',
                        message=message,
                        context=context,
                        need_response=True,
                        reply_markup=old_reply_markup,
                    )

            return await callback(update, context)

    return wrapper
