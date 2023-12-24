from telegram import Update
from telegram.ext import ContextTypes

from function.date_time import utc_to_brazil_datetime


def print_basic_infos(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print('@PRINT_BASIC_INFOS')
        chat_id = update.effective_chat.id
        chat_name = update.effective_chat.effective_name
        user_id = update.effective_user.id
        user_name = update.effective_user.name
        date = update.effective_message.date
        date = utc_to_brazil_datetime(date)

        print(f'\tData: {date}')
        print(
            f'\t{callback.__name__}.start chat.id: {chat_id} '
            f'({chat_name})'
        )
        print(
            f'\t{callback.__name__}.start user_id: {user_id} '
            f'({user_name})'
        )

        return await callback(update, context)

    return wrapper
