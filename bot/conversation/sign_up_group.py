from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
from telegram.constants import ChatType
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from repository.mongo import GroupConfigurationModel
from rpgram import GroupConfiguration


# Stages
START_ROUTES, END_ROUTES = range(2)

# Callback Data
YES = 'yes'
NO = "no"

COMMANDS = [
    'creategroupaccount', 'criarcontagrupo', 'signupgroup', 'cadastrargrupo',
    'creategroup', 'criargrupo'
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('update.effective_chat.id:', update.effective_chat.id)
    print('update.effective_user.id:', update.effective_user.id)

    group_config_model = GroupConfigurationModel()
    chat_id = update.effective_chat.id
    chat_name = update.effective_chat.effective_name
    user_name = update.effective_user.name

    if update.effective_chat.type == ChatType.PRIVATE:
        await update.message.reply_text(
            'Use este comando em um grupo para cadastrá-lo.'
        )
        return ConversationHandler.END
    elif (group_config := group_config_model.get(chat_id)):
        await update.message.reply_text(
            f'Olá {user_name}, Bem-vindo(a) de volta!\n'
            f'O grupo "{chat_name}" já está cadastrado.\n\n'
            f'{group_config}'
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
        'Gostaria de Cadastrar este Grupo?',
        reply_markup=reply_markup,
    )
    context.user_data['response'] = response

    return START_ROUTES


async def create_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_name = update.effective_chat.effective_name
    group_config_model = GroupConfigurationModel()

    if not (group_config := group_config_model.get(chat_id)):
        group_config = GroupConfiguration(
            name=chat_name,
            chat_id=chat_id,
        )
        group_config_model.save(group_config)
        group_config = group_config_model.get(chat_id)

    query = update.callback_query

    await query.answer('Cadastrado com sucesso!')
    await query.edit_message_text(
        "Grupo cadastrado com sucesso!\n\n"
        f'{group_config}',
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_text = "Tchau! Você pode criar uma conta para o grupo mais tarde."

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


SIGNUP_GROUP_HANDLER = ConversationHandler(
    entry_points=[
        CommandHandler("startgroup", start),
        CommandHandler("criargrupo", start),
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