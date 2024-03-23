'''
Módulo responsável por gerenciar as requisiçães de visualização das 
informações dos jogadores.
'''


from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)

from bot.constants.sign_up_player import COMMANDS as sign_up_player_commands
from bot.constants.view_player import (
    COMMANDS,
    REFRESH_VIEW_PLAYER_PATTERN,
    SECTION_TEXT_PLAYER
)
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.functions.chat import (
    get_random_refresh_text,
    get_refresh_close_keyboard
)
from bot.decorators import print_basic_infos, need_singup_player
from bot.functions.general import get_attribute_group_or_player
from constant.text import SECTION_HEAD_PLAYER_END, SECTION_HEAD_PLAYER_START
from function.text import create_text_in_box

from repository.mongo import PlayerModel


@print_basic_infos
@need_singup_player
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    player_model = PlayerModel()
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    silent = get_attribute_group_or_player(chat_id, 'silent')
    query = update.callback_query

    if query:
        data = eval(query.data)
        refresh = data.get(REFRESH_VIEW_PLAYER_PATTERN, False)

    if (player := player_model.get(user_id)):
        text = f'{player}'
        reply_markup = get_refresh_close_keyboard(
            user_id=user_id,
            refresh_data=REFRESH_VIEW_PLAYER_PATTERN,
        )

        if query:
            if refresh:
                '''"refresh_text" é usado para modificar a mensagem de maneira
                aleatória para tentar evitar um erro (BadRequest)
                quando não há mudanças no "text" usado na
                função "edit_message_text".'''
                refresh_text = get_random_refresh_text()
                text = (
                    f'{refresh_text}\n'
                    f'{text}'
                )
            text = create_text_in_box(
                text=text,
                section_name=SECTION_TEXT_PLAYER,
                section_start=SECTION_HEAD_PLAYER_START,
                section_end=SECTION_HEAD_PLAYER_END,
                clean_func=None
            )
            await query.edit_message_text(
                text,
                reply_markup=reply_markup,
            )
        else:
            text = create_text_in_box(
                text=text,
                section_name=SECTION_TEXT_PLAYER,
                section_start=SECTION_HEAD_PLAYER_START,
                section_end=SECTION_HEAD_PLAYER_END,
                clean_func=None
            )
            await update.effective_message.reply_text(
                text,
                disable_notification=silent,
                reply_markup=reply_markup,
                allow_sending_without_reply=True
            )
    else:
        await update.effective_message.reply_text(
            f'Você ainda não está cadastrado!\n'
            f'Cadastre-se com o comando /{sign_up_player_commands[0]}.',
            disable_notification=silent,
            allow_sending_without_reply=True
        )

VIEW_PLAYER_HANDLERS = [
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
    ),
    CallbackQueryHandler(
        start, pattern=fr'^{{"{REFRESH_VIEW_PLAYER_PATTERN}":1'
    ),
]
