'''
Módulo responsável por gerenciar as requisiçães de visualização de 
informações dos grupos.
'''


from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)

from bot.constants.view_group import COMMANDS
from bot.constants.filters import (
    BASIC_COMMAND_IN_GROUP_FILTER,
    PREFIX_COMMANDS
)
from bot.conversations.close import get_close_keyboard
from bot.decorators import print_basic_infos, need_singup_group
from bot.functions.general import get_attribute_group_or_player

from repository.mongo import GroupModel


@print_basic_infos
@need_singup_group
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    group_model = GroupModel()
    chat_id = update.effective_chat.id
    silent = get_attribute_group_or_player(chat_id, 'silent')

    if (group := group_model.get(chat_id)):
        await update.effective_message.reply_text(
            f'{group}',
            disable_notification=silent,
            reply_markup=get_close_keyboard(None)
        )


VIEW_GROUP_HANDLERS = [
    PrefixHandler(
        PREFIX_COMMANDS,
        COMMANDS,
        start,
        BASIC_COMMAND_IN_GROUP_FILTER
    ),
    CommandHandler(
        COMMANDS,
        start,
        BASIC_COMMAND_IN_GROUP_FILTER
    )
]
