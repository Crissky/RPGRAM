'''
Módulo responsável por criar uma nova conta de jogador.
'''


from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    PrefixHandler
)
from bot.conversation.constants import (
    BASIC_COMMAND_FILTER,
    PREFIX_COMMANDS
)
from bot.decorators import print_basic_infos

from repository.mongo import PlayerModel
from rpgram import Player


# ROUTES
START_ROUTES, END_ROUTES = range(2)

# CALLBACK DATA
CALLBACK_TEXT_YES = 'yes'
CALLBACK_TEXT_NO = "no"

COMMANDS = ['criarconta', 'signup']


@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    player_model = PlayerModel()
    user_name = update.effective_user.name
    player_id = update.effective_user.id

    if (player := player_model.get(player_id)):
        await update.effective_message.reply_text(
            f'Olá {user_name}, Bem-vindo(a) de volta!\n'
            f'Vocé já possui uma conta.\n\n'
            f'{player}'
        )
        return ConversationHandler.END

    inline_keyboard = [
        [
            InlineKeyboardButton("Sim", callback_data=CALLBACK_TEXT_YES),
            InlineKeyboardButton("Não", callback_data=CALLBACK_TEXT_NO),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    response = await update.effective_message.reply_text(
        'Seja Bem-vindo, Aventureiro(a).\n'
        'Gostaria de Criar uma Conta?',
        reply_markup=reply_markup,
    )
    context.user_data['response'] = response

    return START_ROUTES


# START_ROUTES
@print_basic_infos
async def create_account(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    user_name = update.effective_user.name
    player_id = update.effective_user.id
    player_model = PlayerModel()
    player = Player(user_name, player_id)
    player_model.save(player)
    player = player_model.get(player_id)
    query = update.callback_query

    await query.answer('Cadastrado com sucesso!')
    await query.edit_message_text(
        "Conta criada com sucesso!\n\n"
        f'{player}',
    )

    return ConversationHandler.END


# START_ROUTES
@print_basic_infos
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    new_text = "Tchau! Você pode criar uma conta mais tarde."

    if 'response' in context.user_data:
        response = context.user_data['response']
        chat_id = response.chat_id
        message_id = response.id
        print(
            f'{__name__}.cancel():',
            f'chat_id: {chat_id}, message_id: {message_id}'
        )
        await update.get_bot().edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=new_text,
        )
        del context.user_data['response']
    elif update.callback_query:
        # await update.callback_query.answer()
        await update.callback_query.edit_message_text(new_text)

    return ConversationHandler.END


SIGNUP_PLAYER_HANDLER = ConversationHandler(
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
    fallbacks=[CommandHandler("cancel", cancel)],
)
