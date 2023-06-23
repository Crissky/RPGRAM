'''
Módulo responsável por gerenciar o comando de configuração de grupo.
'''


from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import CommandHandler, ContextTypes, PrefixHandler

from bot.constants.config_group import COMMANDS
from bot.conversation.filters import (
    BASIC_COMMAND_IN_GROUP_FILTER,
    PREFIX_COMMANDS
)
from bot.decorators import print_basic_infos, need_are_admin, need_singup_group

from repository.mongo import GroupModel


@print_basic_infos
@need_singup_group
@need_are_admin
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_chat_action(ChatAction.TYPING)
    group_model = GroupModel()
    chat_id = update.effective_chat.id
    args = context.args
    group = group_model.get(chat_id)

    if len(args) == 2:
        attribute = args[0]
        value = args[1]
        try:
            group[attribute] = value
            group_model.save(group)
            await update.effective_message.reply_text(
                f'Configurado "{attribute}" para "{value}".\n\n'
                f'{group}'
            )
        except (KeyError, ValueError) as error:
            await update.effective_message.reply_text(
                str(error)
            )
    elif 'default' in args or 'padrao' in args or 'padrão' in args:
        group['VERBOSE'] = 'false'
        group['START_TIME'] = '6'
        group['END_TIME'] = '20'
        group['MULTIPLIER_XP'] = '1'
        group['CHAR_MULTIPLIER_XP'] = '1'
        group_model.save(group)
        await update.effective_message.reply_text(
            f'Configurado para os valores padrões.\n\n'
            f'{group}'
        )
    elif len(args) != 2:
        await update.effective_message.reply_text(
            'Envie o ATRIBUTO e o VALOR que deseja configurar.'
        )


CONFIG_GROUP_HANDLERS = [
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
