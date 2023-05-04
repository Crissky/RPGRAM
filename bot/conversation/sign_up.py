from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["Sim", "Não"]]
    reply_markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, input_field_placeholder="Sim ou Não?"
    )
    await update.message.reply_text(
        "Seja Bem-vindo, Aventureiro(a).\n"
        "Gostaria de Criar uma Conta?",
        reply_markup=reply_markup,
    )
    return ConversationHandler.END


SIGNUP_HANDLER = ConversationHandler(
    entry_points=[
        CommandHandler("start", start), CommandHandler("criarconta", start),
        MessageHandler(
            filters.Regex(r'^!(createaccount|criarconta|signup)$'), start
        )
    ],
    states={},
    fallbacks=[],
)
