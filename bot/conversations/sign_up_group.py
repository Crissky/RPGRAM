'''
Módulo responsável por criar a conta de um grupo para armazenar as 
informações configurações do grupo.
'''


from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
from telegram.constants import ChatType
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    PrefixHandler,
)

from bot.constants.sign_up_group import (
    COMMANDS,
    CALLBACK_TEXT_YES,
    CALLBACK_TEXT_NO,
)
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.decorators import print_basic_infos

from bot.functions.chat import answer
from constant.time import TEN_MINUTES_IN_SECONDS

from repository.mongo import GroupModel

from rpgram import Group


# ROUTES
START_ROUTES = range(1)


@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_model = GroupModel()
    chat_id = update.effective_chat.id
    chat_name = update.effective_chat.effective_name
    user_name = update.effective_user.name

    if update.effective_chat.type == ChatType.PRIVATE:
        await update.effective_message.reply_text(
            'Use este comando em um grupo para cadastrá-lo.',
            allow_sending_without_reply=True
        )
        return ConversationHandler.END
    elif (group_config := group_model.get(chat_id)):
        await update.effective_message.reply_text(
            f'Olá {user_name}, Bem-vindo(a) de volta!\n'
            f'O grupo "{chat_name}" já está cadastrado.\n\n'
            f'{group_config}',
            allow_sending_without_reply=True
        )
        return ConversationHandler.END

    inline_keyboard = [
        [
            InlineKeyboardButton('Sim', callback_data=CALLBACK_TEXT_YES),
            InlineKeyboardButton('Não', callback_data=CALLBACK_TEXT_NO),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    response = await update.effective_message.reply_text(
        'Seja Bem-vindo, Aventureiro(a).\n'
        'Gostaria de Cadastrar este Grupo?',
        reply_markup=reply_markup,
        allow_sending_without_reply=True
    )
    context.user_data['response'] = response

    return START_ROUTES


# START_ROUTES
@print_basic_infos
async def create_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_name = update.effective_chat.effective_name
    group_model = GroupModel()

    if not (group_config := group_model.get(chat_id)):
        group_config = Group(
            name=chat_name,
            chat_id=chat_id,
        )
        group_model.save(group_config)
        group_config = group_model.get(chat_id)

    query = update.callback_query

    await answer(query=query, text='Cadastrado com sucesso!')
    await query.edit_message_text(
        'Grupo cadastrado com sucesso!\n\n'
        f'{group_config}',
    )

    return ConversationHandler.END


# START_ROUTES
@print_basic_infos
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_text = 'Tchau! Você pode criar uma conta para o grupo mais tarde.'

    if 'response' in context.user_data:
        response = context.user_data['response']
        chat_id = response.chat_id
        message_id = response.id
        print(
            f'{__name__}.cancel()',
            f'chat_id: {chat_id}, message_id: {message_id}'
        )
        await update.get_bot().edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=new_text,
        )
        del context.user_data['response']
    elif update.callback_query:
        query = update.callback_query
        await query.edit_message_text(new_text)

    return ConversationHandler.END


SIGNUP_GROUP_HANDLER = ConversationHandler(
    entry_points=[
        PrefixHandler(
            PREFIX_COMMANDS,
            COMMANDS,
            start,
            BASIC_COMMAND_FILTER
        ),
        CommandHandler(COMMANDS, start, BASIC_COMMAND_FILTER),
    ],
    states={
        START_ROUTES: [
            CallbackQueryHandler(
                create_account, pattern=f'^{CALLBACK_TEXT_YES}$'
            ),
            CallbackQueryHandler(cancel, pattern=f'^{CALLBACK_TEXT_NO}$')
        ]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    conversation_timeout=TEN_MINUTES_IN_SECONDS,
    allow_reentry=True
)
