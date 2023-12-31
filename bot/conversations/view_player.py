'''
Módulo responsável por gerenciar as requisiçães de visualização das 
informações dos jogadores.
'''


from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)

from bot.constants.sign_up_player import COMMANDS as sign_up_player_commands
from bot.constants.view_player import COMMANDS, SECTION_TEXT_PLAYER
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.conversations.close import get_close_keyboard
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

    if (player := player_model.get(user_id)):
        text = create_text_in_box(
            text=f'{player}',
            section_name=SECTION_TEXT_PLAYER,
            section_start=SECTION_HEAD_PLAYER_START,
            section_end=SECTION_HEAD_PLAYER_END,
            clean_func=None
        )

        await update.effective_message.reply_text(
            text,
            disable_notification=silent,
            reply_markup=get_close_keyboard(user_id=user_id)
        )
    else:
        await update.effective_message.reply_text(
            f'Você ainda não está cadastrado!\n'
            f'Cadastre-se com o comando /{sign_up_player_commands[0]}.',
            disable_notification=silent
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
    )
]
