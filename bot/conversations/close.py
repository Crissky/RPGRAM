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
    ESCAPED_CALLBACK_CLOSE,
    LEFT_CLOSE_BUTTON_TEXT,
    REFRESH_BUTTON_TEXT,
    RIGHT_CLOSE_BUTTON_TEXT
)
from bot.decorators.char import skip_if_no_have_char
from bot.decorators.print import print_basic_infos
from rpgram.enums import FaceEmojiEnum


@print_basic_infos
@skip_if_no_have_char
async def close(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    query = update.callback_query

    if query:
        data = eval(query.data)
        data_user_id = data['user_id']

        # Não executa se outro usuário mexer na bolsa
        if data_user_id != user_id and data_user_id is not None:
            await query.answer(text=ACCESS_DENIED, show_alert=True)
        else:
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
    refresh_data: str = 'refresh'
) -> List[InlineKeyboardButton]:
    return [
        InlineKeyboardButton(
            REFRESH_BUTTON_TEXT,
            callback_data=(
                f'{{"{refresh_data}":1,'
                f'"user_id":{user_id}}}'
            )
        ),
        get_close_button(user_id=user_id, right_icon=True)
    ]


def get_random_refresh_text() -> str:
    emoji = choice(list(FaceEmojiEnum)).value
    return f'Atualizado{emoji}'


def get_close_keyboard(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        get_close_button(user_id=user_id)
    ]])


def get_refresh_close_keyboard(
    user_id: int,
    refresh_data: str = 'refresh'
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        get_refresh_close_button(user_id=user_id, refresh_data=refresh_data)
    ])


CLOSE_MSG_HANDLER = CallbackQueryHandler(
    close,
    pattern=f'^{{"command":"{ESCAPED_CALLBACK_CLOSE}"'
)
