'''
Módulo responsável por exibir algumas variáveis de contexto
'''


from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PrefixHandler
)

from bot.constants.debug import COMMANDS, DEBUFF_COMMANDS
from bot.constants.filters import (
    BASIC_COMMAND_FILTER,
    PREFIX_COMMANDS,
)
from bot.decorators import (
    skip_if_no_have_char,
    skip_if_no_singup_player,
    print_basic_infos,
)
from bot.functions.char import add_conditions
from bot.functions.general import get_attribute_group_or_player
from function.text import escape_basic_markdown_v2
from rpgram.conditions.debuff import DEBUFFS


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


@skip_if_no_singup_player
@skip_if_no_have_char
@print_basic_infos
async def get_random_debuff(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    args = context.args

    report = add_conditions(*DEBUFFS, user_id=user_id)
    char = report['char']
    text = escape_basic_markdown_v2(report['text'])
    text += char.get_all_sheets(verbose=False, markdown=True)
    await update.effective_message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN_V2,
        disable_notification=silent,
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
    ),
    PrefixHandler(
        PREFIX_COMMANDS,
        DEBUFF_COMMANDS,
        get_random_debuff,
        BASIC_COMMAND_FILTER
    ),
    CommandHandler(
        DEBUFF_COMMANDS,
        get_random_debuff,
        BASIC_COMMAND_FILTER
    ),
]
