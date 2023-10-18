'''
Módulo responsável por exibir algumas variáveis de contexto
'''


from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PrefixHandler
)

from bot.constants.debug import COMMANDS
from bot.constants.filters import (
    BASIC_COMMAND_FILTER,
    PREFIX_COMMANDS,
)
from bot.decorators import (
    skip_if_no_have_char,
    skip_if_no_singup_player,
    print_basic_infos,
)
from bot.functions.general import get_attribute_group_or_player


@skip_if_no_singup_player
@skip_if_no_have_char
@print_basic_infos
async def start_debug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    args = context.args

    if isinstance(args, list) and args[0] in ['chat', 'chat_data']:
        chat_data = context.chat_data
        text = 'Conteúdo de "context.chat_data":\n\n'
        for key, value in chat_data.items():
            text += f'{key}: {value}\n'
    else:
        text = f'"{args}" não é um argumento válido.'

    await update.effective_message.reply_text(
        text,
        disable_notification=silent
    )


DEBUG_HANDLERS = [
    PrefixHandler(
        PREFIX_COMMANDS,
        COMMANDS,
        start_debug,
        BASIC_COMMAND_FILTER
    ),
    CommandHandler(
        COMMANDS,
        start_debug,
        BASIC_COMMAND_FILTER
    )
]
