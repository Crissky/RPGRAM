from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    PrefixHandler
)

from bot.conversation.constants import (
    BASIC_COMMAND_IN_GROUP_FILTER,
    PREFIX_COMMANDS
)
from bot.decorators import need_have_char
from bot.decorators import print_basic_infos

COMMANDS = ['duel', 'duelo']


@need_have_char
@print_basic_infos
async def battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Comando no implementado.")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    return ConversationHandler.END


BATTLE_HANDLER = ConversationHandler(
    entry_points=[
        PrefixHandler(
            PREFIX_COMMANDS,
            COMMANDS,
            battle,
            BASIC_COMMAND_IN_GROUP_FILTER
        ),
        CommandHandler(COMMANDS, battle, BASIC_COMMAND_IN_GROUP_FILTER),
    ],
    states={},
    fallbacks=[CommandHandler("cancel", cancel)],
)
