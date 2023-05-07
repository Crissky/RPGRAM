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

COMMANDS = ['createaccount', 'criarconta', 'signup']


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player_model = PlayerModel()
    print('update.effective_chat.id:', update.effective_chat.id)
    user_name = update.effective_user.name
    player_id = update.effective_user.id
    if (player := player_model.get(player_id)):
        await update.message.reply_text(
            f'Olá {user_name}, Bem-vindo(a) de volta!\n'
            f'Vocé já possui uma conta.\n\n'
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
    response = await update.message.reply_text(
        'Seja Bem-vindo, Aventureiro(a).\n'
        'Gostaria de Criar uma Conta?',
        reply_markup=reply_markup,
    )
    context.user_data['response'] = response

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
    new_text = "Tchau! Você pode criar uma conta mais tarde."
    if 'response' in context.user_data:
        response = context.user_data['response']
        chat_id = response.chat_id
        message_id = response.id
        print(f'chat_id: {chat_id}, message_id: {message_id}')
        await update.get_bot().edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=new_text,
        )
        del context.user_data['response']
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(new_text)
    return ConversationHandler.END


SIGNUP_PLAYER_HANDLER = ConversationHandler(
    entry_points=[
        CommandHandler("start", start), CommandHandler("criarconta", start),
        MessageHandler(
            filters.Regex(rf'^!({"|".join(COMMANDS)})$'), start
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
