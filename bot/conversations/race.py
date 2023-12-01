from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)
from bot.conversations.close import get_close_button
from bot.functions.general import get_attribute_group_or_player
from bot.functions.keyboard import reshape_row_buttons

from bot.constants.race import ACCESS_DENIED, COMMANDS
from repository.mongo import RaceModel


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    args = context.args
    query = update.callback_query
    silent = get_attribute_group_or_player(chat_id, 'silent')

    _all = None
    text = 'Escolha uma raça para exibir suas informações.'
    if query:
        data = eval(query.data)
        data_user_id = data['user_id']
        race_name = data['race_name']
        _all = data['_all']

        # Não executa se outro usuário mexer na bolsa
        if data_user_id != user_id:
            await query.answer(text=ACCESS_DENIED, show_alert=True)
            return None

        race_model = RaceModel()
        race = race_model.get(race_name)
        text = race.get_sheet(verbose=True)
        text += f'\nDESCRIÇÃO: {race.description}'

    if _all is True or (args and args[0] in ['all', 'a', 'todos', 't']):
        is_all = True
    else:
        is_all = False

    race_buttons = get_race_buttons(user_id=user_id, _all=is_all)
    close_button = get_close_button(user_id=user_id)
    reply_markup = InlineKeyboardMarkup(
        race_buttons  + [[close_button]]
    )
    if query:
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup,
        )
    else:
        await update.effective_message.reply_text(
            text=text,
            reply_markup=reply_markup,
            disable_notification=silent,
        )


def get_race_buttons(
    user_id: int,
    _all: bool = False
) -> List[List[InlineKeyboardButton]]:
    race_model = RaceModel()
    race_buttons = []
    query = {} if _all is True else {'enemy': False}
    race_names = race_model.get_all(query=query, fields=['name'])

    for race_name in race_names:
        race_buttons.append(
            InlineKeyboardButton(
                text=race_name,
                callback_data=(
                    f'{{"race_name":"{race_name}",'
                    f'"_all": {_all},'
                    f'"user_id":{user_id}}}'
                )
            )
        )

    return reshape_row_buttons(
        race_buttons,
        buttons_per_row=3
    )


RACES_HANDLERS = [
    PrefixHandler(
        PREFIX_COMMANDS,
        COMMANDS,
        start,
        BASIC_COMMAND_FILTER
    ),
    CommandHandler(
        COMMANDS,
        start,
        BASIC_COMMAND_FILTER
    ),
    CallbackQueryHandler(start, pattern=r'^{"race_name":'),
]
