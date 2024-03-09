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
from bot.conversations.close import get_close_keyboard
from bot.decorators import (
    skip_if_no_have_char,
    skip_if_no_singup_player,
    print_basic_infos,
)
from bot.functions.char import add_conditions
from bot.functions.config import get_attribute_group
from bot.functions.general import get_attribute_group_or_player
from constant.text import TEXT_SEPARATOR
from function.text import escape_basic_markdown_v2
from repository.mongo.populate.enemy import create_random_enemies
from rpgram.conditions.debuff import DEBUFFS
from rpgram.conditions.factory import factory_condition


@skip_if_no_singup_player
@skip_if_no_have_char
@print_basic_infos
async def start_debug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    args = context.args

    if len(args) > 0 and args[0] in ['chat', 'chat_data']:
        chat_data = context.chat_data
        text = 'Conteúdo de "context.chat_data":\n\n'
        for key, value in chat_data.items():
            text += f'{key}: {value}\n'
    elif len(args) > 0 and args[0] in ['enemy', 'inimigo']:
        group_level = get_attribute_group(chat_id, 'group_level')
        enemy_list = create_random_enemies(group_level=group_level)
        text = f'{TEXT_SEPARATOR}\n\n'.join(
            enemy.get_all_sheets()
            for enemy in enemy_list
        )
    else:
        text = f'"{args}" não é um argumento válido.'

    text = escape_basic_markdown_v2(text)
    await update.effective_message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN_V2,
        disable_notification=silent,
        reply_markup=get_close_keyboard(None),
        allow_sending_without_reply=True
    )


@skip_if_no_singup_player
@skip_if_no_have_char
@print_basic_infos
async def get_random_debuff(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    ''' Comando que adiciona debuffs no personagem do jogador.
    Caso não seja passado nenhum argumento, adiciona 1 nível de 
    todos os debuffs.
    O primeiro argumento é o nome do debuff, o segundo é o nível.
    Se o nível não for passado, será considerado 1.
    '''

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    args = context.args

    if args:
        condition_name = args.pop(0).title()
        condition_level = args.pop(0) if args else 1
        condition_level = abs(int(condition_level))
        condition = factory_condition(
            condition_name=condition_name,
            level=condition_level
        )
        report = add_conditions(condition, user_id=user_id)
    else:
        report = add_conditions(*DEBUFFS, user_id=user_id)
    char = report['char']
    text = report['text']
    text += char.get_all_sheets(verbose=False, markdown=True)
    text = escape_basic_markdown_v2(text)
    await update.effective_message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN_V2,
        disable_notification=silent,
        reply_markup=get_close_keyboard(user_id=user_id),
        allow_sending_without_reply=True
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
