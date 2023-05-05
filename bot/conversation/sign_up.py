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
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from repository.mongo import PlayerModel
from rpgram import Player


# Stages
START_ROUTES, END_ROUTES = range(2)

# Callback Data
YES = 'yes'
NO = "no"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player_model = PlayerModel()
    print('update.effective_chat.id:', update.effective_chat.id)
    user_name = update.effective_user.name
    player_id = update.effective_user.id
    if (player := player_model.get(player_id)):
        await update.message.reply_text(
            f'Olá {user_name}, Bem-vindo(a) de volta!\n'
            f'Vocé já possui uma conta criada.\n\n'
            f'{player}'
        )

        return ConversationHandler.END

    inline_keyboard = [
        [
            InlineKeyboardButton("Sim", callback_data=YES),
            InlineKeyboardButton("Não", callback_data=NO),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    await update.message.reply_text(
        'Seja Bem-vindo, Aventureiro(a).\n'
        'Gostaria de Criar uma Conta?',
        reply_markup=reply_markup,
    )
    return START_ROUTES


async def create_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player_model = PlayerModel()
    user_name = update.effective_user.name
    player_id = update.effective_user.id
    player = Player(user_name, player_id)
    player_model.save(player)
    player = player_model.get(player_id)
    query = update.callback_query

    await query.answer()
    await query.edit_message_text(
        "Conta criada com sucesso!\n\n"
        f'{player}',
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "Tchau! Você pode criar uma conta mais tarde.",
            reply_markup=ReplyKeyboardRemove()
        )
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            "Tchau! Vocé pode criar uma conta mais tarde."
        )
    return ConversationHandler.END


SIGNUP_HANDLER = ConversationHandler(
    entry_points=[
        CommandHandler("start", start), CommandHandler("criarconta", start),
        MessageHandler(
            filters.Regex(r'^!(createaccount|criarconta|signup)$'), start
        )
    ],
    states={
        START_ROUTES: [
            CallbackQueryHandler(create_account, pattern=f'^{YES}$'),
            CallbackQueryHandler(cancel, pattern=f'^{NO}$')
        ]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
