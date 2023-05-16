from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PrefixHandler
)

from bot.conversation.constants import (
    BASIC_COMMAND_FILTER,
    PREFIX_COMMANDS,
)
from bot.decorators import need_have_char
from repository.mongo import PlayerCharacterModel

COMMANDS = ['stats', 'add_stats']


@need_have_char
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_chat_action(ChatAction.TYPING)
    player_char_model = PlayerCharacterModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    print(f'{__name__}.start', 'chat.id:', chat_id)
    print(f'{__name__}.start', 'user_id:', user_id)

    args = context.args
    player_char = player_char_model.get(user_id)
    text = ''
    if len(args) == 2:
        attribute = args[0]
        value = args[1]
        try:
            player_char.base_stats[attribute] = value
            player_char_model.save(player_char)
            text = (
                f'Adicionado {value} ponto(s) no atributo "{attribute}".\n\n'
            )
        except (KeyError, ValueError) as error:
            await update.effective_message.reply_text(
                str(error)
            )
            return
    elif len(args) > 2:
        await update.effective_message.reply_text(
            'Envie somente o ATRIBUTO e o VALOR que deseja adicionar.'
        )
        return

    await update.effective_message.reply_text(
        f'{text}'
        f'{player_char.base_stats}'
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
