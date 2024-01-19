from random import choice
from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
)

from bot.constants.close import (
    ACCESS_DENIED,
    CALLBACK_CLOSE,
    DETAIL_BUTTON_TEXT,
    ESCAPED_CALLBACK_CLOSE,
    LEFT_CLOSE_BUTTON_TEXT,
    REFRESH_BUTTON_TEXT,
    RIGHT_CLOSE_BUTTON_TEXT
)
from bot.decorators import (
    skip_if_no_have_char,
    alert_if_not_chat_owner,
    print_basic_infos
)
from rpgram.enums import FaceEmojiEnum


@alert_if_not_chat_owner(alert_text=ACCESS_DENIED)
@print_basic_infos
@skip_if_no_have_char
async def close(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    if query:
        await query.answer('Fechando conversa...')
        await query.delete_message()


def get_close_button(
    user_id: int,
    text: str = None,
    right_icon: bool = False,
) -> InlineKeyboardButton:
    if text is None:
        text = LEFT_CLOSE_BUTTON_TEXT
        if right_icon:
            text = RIGHT_CLOSE_BUTTON_TEXT

    return InlineKeyboardButton(
        text=text,
        callback_data=(
            f'{{"command":"{CALLBACK_CLOSE}",'
            f'"user_id":{user_id}}}'
        )
    )


def get_refresh_close_button(
    user_id: int,
    refresh_data: str = 'refresh',
    to_detail: bool = False,
) -> List[InlineKeyboardButton]:
    button_list = []
    button_list.append(
        InlineKeyboardButton(
            REFRESH_BUTTON_TEXT,
            callback_data=(
                f'{{"{refresh_data}":1,'
                f'"user_id":{user_id}}}'
            )
        )
    )
    if to_detail:
        button_list.append(
            InlineKeyboardButton(
                DETAIL_BUTTON_TEXT,
                callback_data=(
                    f'{{"{refresh_data}":1,"verbose":"v",'
                    f'"user_id":{user_id}}}'
                )
            )
        )
    button_list.append(get_close_button(user_id=user_id, right_icon=True))

    return button_list


def get_random_refresh_text() -> str:
    emoji = choice(list(FaceEmojiEnum)).value
    return f'Atualizado{emoji}'


def get_close_keyboard(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        get_close_button(user_id=user_id)
    ]])


def get_refresh_close_keyboard(
    user_id: int,
    refresh_data: str = 'refresh',
    to_detail: bool = False,
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        get_refresh_close_button(
            user_id=user_id,
            refresh_data=refresh_data,
            to_detail=to_detail
        )
    ])


CLOSE_MSG_HANDLER = CallbackQueryHandler(
    close,
    pattern=f'^{{"command":"{ESCAPED_CALLBACK_CLOSE}"'
)
