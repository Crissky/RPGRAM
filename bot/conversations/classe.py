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
from bot.decorators.player import alert_if_not_chat_owner
from bot.functions.general import get_attribute_group_or_player
from bot.functions.keyboard import reshape_row_buttons

from bot.constants.classe import ACCESS_DENIED, COMMANDS
from repository.mongo import ClasseModel


@alert_if_not_chat_owner(alert_text=ACCESS_DENIED)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    args = context.args
    query = update.callback_query
    silent = get_attribute_group_or_player(chat_id, 'silent')
    _all = None
    text = 'Escolha uma classe para exibir suas informações.'

    if query:
        data = eval(query.data)
        classe_name = data['classe_name']
        _all = data['_all']
        classe_model = ClasseModel()
        classe = classe_model.get(classe_name)
        text = classe.get_sheet(verbose=True)
        text += f'\nDESCRIÇÃO: {classe.description}'

    if _all is True or (args and args[0] in ['all', 'a', 'todos', 't']):
        is_all = True
    else:
        is_all = False

    classe_buttons = get_classe_buttons(user_id=user_id, _all=is_all)
    close_button = get_close_button(user_id=user_id)
    reply_markup = InlineKeyboardMarkup(
        classe_buttons + [[close_button]]
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


def get_classe_buttons(
    user_id: int,
    _all: bool = False
) -> List[List[InlineKeyboardButton]]:
    classe_model = ClasseModel()
    classe_buttons = []
    query = {} if _all is True else {'enemy': False}
    classe_names = classe_model.get_all(query=query, fields=['name'])

    for classe_name in classe_names:
        classe_buttons.append(
            InlineKeyboardButton(
                text=classe_name,
                callback_data=(
                    f'{{"classe_name":"{classe_name}",'
                    f'"_all": {_all},'
                    f'"user_id":{user_id}}}'
                )
            )
        )

    return reshape_row_buttons(
        classe_buttons,
        buttons_per_row=3
    )


CLASSES_HANDLERS = [
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
    CallbackQueryHandler(start, pattern=r'^{"classe_name":'),
]
