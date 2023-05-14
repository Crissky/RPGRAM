'''
Arquivo responsável por gerenciar as requisiçães de visualização de 
informações dos grupos.
'''

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PrefixHandler,
    filters,
)
from bot.conversation.constants import BASIC_COMMAND_FILTER, PREFIX_COMMANDS

from bot.conversation.sign_up_group import COMMANDS as sign_up_group_commands
from repository.mongo import GroupConfigurationModel


COMMANDS = ['grupo', 'group']


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    group_config_model = GroupConfigurationModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    print(f'{__name__}.start', 'chat.id:', chat_id)
    print(f'{__name__}.start', 'user_id:', user_id)

    if (group := group_config_model.get(chat_id)):
        await update.effective_message.reply_text(f'{group}')
    else:
        await update.effective_message.reply_text(
            f'Grupo não Cadastrado!\n'
            f'Cadastre o grupo com o comando /{sign_up_group_commands[0]}.'
        )

VIEW_GROUP_HANDLERS = [
    PrefixHandler(
        PREFIX_COMMANDS,
        COMMANDS,
        start,
        filters.ChatType.GROUPS & BASIC_COMMAND_FILTER
    ),
    CommandHandler(
        COMMANDS,
        start,
        filters.ChatType.GROUPS & BASIC_COMMAND_FILTER
    )
]
