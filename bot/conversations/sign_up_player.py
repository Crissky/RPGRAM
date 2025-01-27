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

from bot.constants.sign_up_player import COMMANDS
from bot.constants.sign_up_player import CALLBACK_TEXT_YES
from bot.constants.sign_up_player import CALLBACK_TEXT_NO
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.decorators import print_basic_infos

from bot.decorators.group import need_singup_group
from bot.functions.chat import (
    MIN_AUTODELETE_TIME,
    answer,
    call_telegram_message_function,
    edit_message_text
)
from bot.functions.config import update_total_players
from constant.time import TEN_MINUTES_IN_SECONDS

from repository.mongo import PlayerModel

from rpgram import Player


# ROUTES
START_ROUTES, END_ROUTES = range(2)


@need_singup_group
@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    player_model = PlayerModel()
    user_name = update.effective_user.name
    player_id = update.effective_user.id

    player: Player = player_model.get(player_id)
    if player:
        reply_text_kwargs = dict(
            text=(
                f'Olá {user_name}, Bem-vindo(a) de volta!\n'
                f'Vocé já possui uma conta.\n\n'
                f'{player}'
            ),
            allow_sending_without_reply=True
        )
        await call_telegram_message_function(
            function_caller='SIGN_UP_PLAYER.START()',
            function=update.effective_message.reply_text,
            context=context,
            need_response=False,
            skip_retry=False,
            auto_delete_message=MIN_AUTODELETE_TIME,
            **reply_text_kwargs,
        )
        return ConversationHandler.END

    inline_keyboard = [
        [
            InlineKeyboardButton("Sim", callback_data=CALLBACK_TEXT_YES),
            InlineKeyboardButton("Não", callback_data=CALLBACK_TEXT_NO),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    reply_text_kwargs = dict(
        text=(
            'Seja Bem-vindo, Aventureiro(a).\n'
            'Gostaria de Criar uma Conta?'
        ),
        reply_markup=reply_markup,
        allow_sending_without_reply=True
    )
    response = await call_telegram_message_function(
        function_caller='SIGN_UP_PLAYER.START()',
        function=update.effective_message.reply_text,
        context=context,
        need_response=True,
        skip_retry=False,
        auto_delete_message=MIN_AUTODELETE_TIME,
        **reply_text_kwargs,
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
    chat_id = update.effective_chat.id
    message_id = update.effective_message.id
    player_model = PlayerModel()
    player = Player(user_name, player_id)
    player.add_chat_id(chat_id)
    player_model.save(player)
    player: Player = player_model.get(player_id)
    query = update.callback_query

    await answer(query=query, text='Cadastrado com sucesso!')
    new_text = (
        f'Conta criada com sucesso!\n\n'
        f'{player}'
    )
    await edit_message_text(
        function_caller='SIGN_UP_PLAYER.CREATE_ACCOUNT()',
        new_text=new_text,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=False,
    )
    update_total_players(chat_id=chat_id)

    return ConversationHandler.END


# START_ROUTES
@print_basic_infos
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    new_text = "Tchau! Você pode criar uma conta mais tarde."
    chat_id = update.effective_chat.id
    message_id = update.effective_message.id

    print(
        f'{__name__}.cancel():',
        f'chat_id: {chat_id}, message_id: {message_id}'
    )
    await edit_message_text(
        function_caller='SIGN_UP_PLAYER.CANCEL()',
        new_text=new_text,
        context=context,
        chat_id=chat_id,
        message_id=message_id,
        need_response=False,
        markdown=False,
    )
    if 'response' in context.user_data:
        del context.user_data['response']

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
    conversation_timeout=TEN_MINUTES_IN_SECONDS,
    allow_reentry=True
)
