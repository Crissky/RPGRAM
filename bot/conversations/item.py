from random import choice

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)
from bot.constants.item import (
    REPLY_TEXTS_FIND_TREASURE_START,
    REPLY_TEXTS_FIND_TREASURE_MIDDLE,
    REPLY_TEXTS_FIND_TREASURE_END,
)

from bot.functions.general import get_attribute_group_or_player


CALLBACK_TEXT_YES = 'get_item'
CALLBACK_TEXT_NO = 'drop_item'

async def job_find_treasure(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    chat_id = job.chat_id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    text = choice(REPLY_TEXTS_FIND_TREASURE_START)
    text += choice(REPLY_TEXTS_FIND_TREASURE_MIDDLE)
    text += choice(REPLY_TEXTS_FIND_TREASURE_END)
    inline_keyboard = [
        [
            InlineKeyboardButton('Investigar', callback_data=CALLBACK_TEXT_YES),
            InlineKeyboardButton('Ignorar', callback_data=CALLBACK_TEXT_NO),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        disable_notification=silent,
        reply_markup=reply_markup,
    )
