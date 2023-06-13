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

from bot.constants.sign_up_group import COMMANDS as sign_up_group_commands
from bot.constants.view_group import COMMANDS
from bot.conversation.filters import (
    BASIC_COMMAND_IN_GROUP_FILTER,
    PREFIX_COMMANDS
)
from bot.decorators import print_basic_infos, need_singup_group

from repository.mongo import GroupConfigurationModel


@print_basic_infos
@need_singup_group
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    group_config_model = GroupConfigurationModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if (group := group_config_model.get(chat_id)):
        await update.effective_message.reply_text(f'{group}')


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
