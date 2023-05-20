from telegram import Update
from telegram.ext import ContextTypes

from functions.datetime import utc_to_brazil_datetime


def print_basic_infos(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print('@PRINT_BASIC_INFOS')
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        date = update.effective_message.date
        date = utc_to_brazil_datetime(date)

        print(f'\tData: {date}')
        print(f'\t{callback.__name__}.start', 'chat.id:', chat_id)
        print(f'\t{callback.__name__}.start', 'user_id:', user_id)

        return await callback(update, context)

    return wrapper
