from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)
from bot.functions.chat import (
    call_telegram_message_function,
    edit_message_text,
    get_close_button
)
from bot.decorators.player import (
    alert_if_not_chat_owner_to_callback_data_to_dict
)
from bot.functions.chat import CALLBACK_KEY_LIST, callback_data_to_dict, callback_data_to_string
from bot.functions.general import get_attribute_group_or_player
from bot.functions.keyboard import reshape_row_buttons

from bot.constants.race import ACCESS_DENIED, COMMANDS
from repository.mongo import RaceModel


@alert_if_not_chat_owner_to_callback_data_to_dict(alert_text=ACCESS_DENIED)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    message_id = update.effective_message.id
    args = context.args
    query = update.callback_query
    silent = get_attribute_group_or_player(chat_id, 'silent')
    _all = None

    text = 'Escolha uma raça para exibir suas informações.'
    if query:
        data = callback_data_to_dict(query.data)
        race_name = data['race_name']
        _all = data['_all']

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
        race_buttons + [[close_button]]
    )
    if query:
        await edit_message_text(
            function_caller='RACE.START()',
            new_text=text,
            context=context,
            chat_id=chat_id,
            message_id=message_id,
            need_response=False,
            markdown=False,
            reply_markup=reply_markup,
        )
    else:
        reply_text_kwargs = dict(
            text=text,
            reply_markup=reply_markup,
            disable_notification=silent,
            allow_sending_without_reply=True
        )
        await call_telegram_message_function(
            function_caller='RACE.START()',
            function=update.effective_message.reply_text,
            context=context,
            need_response=False,
            skip_retry=False,
            **reply_text_kwargs,
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
        callback_data = callback_data_to_string({
            'race_name': race_name,
            '_all': _all,
            'user_id': user_id
        })

        race_buttons.append(
            InlineKeyboardButton(
                text=race_name,
                callback_data=callback_data
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
    CallbackQueryHandler(
        start,
        pattern=fr'^{{{CALLBACK_KEY_LIST.index("race_name")}:'
    ),
]
