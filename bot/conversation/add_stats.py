from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PrefixHandler
)

from bot.conversation.constants import (
    BASIC_COMMAND_FILTER,
    PREFIX_COMMANDS,
)
from bot.decorators import need_have_char, print_basic_infos
from functions.text import escape_markdown_v2
from repository.mongo import CharacterModel


COMMANDS = ['stats', 'add_stats']


@need_have_char
@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_chat_action(ChatAction.TYPING)
    char_model = CharacterModel()
    user_id = update.effective_user.id

    args = context.args
    player_char = char_model.get(user_id)
    text = ''
    verbose = False
    if len(args) == 2:
        attribute = args[0].upper()
        value = args[1]
        try:
            player_char.base_stats[attribute] = value
            char_model.save(player_char)
            text = escape_markdown_v2(
                f'Adicionado "{value}" ponto(s) no atributo "{attribute}".\n\n'
            )
        except (KeyError, ValueError) as error:
            await update.effective_message.reply_text(str(error))
            return
    elif len(args) > 2:
        await update.effective_message.reply_text(
            'Envie somente o ATRIBUTO e o VALOR que deseja adicionar.'
        )
        return
    elif len(args) == 1:
        verbose = 'verbose' == args[0] or 'v' == args[0]

    await update.effective_message.reply_text(
        f'{text}'
        f'{player_char.cs.get_all_sheets(verbose=verbose, markdown=True)}',
        parse_mode=ParseMode.MARKDOWN_V2
    )


ADD_STATS_HANDLERS = [
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
    )
]
