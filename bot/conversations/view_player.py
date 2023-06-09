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
from bot.constants.view_player import COMMANDS
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.decorators import print_basic_infos, need_singup_player
from bot.functions.general import get_attribute_group_or_player

from repository.mongo import PlayerModel


@print_basic_infos
@need_singup_player
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    player_model = PlayerModel()
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    silent = get_attribute_group_or_player(chat_id, 'silent')

    if (player := player_model.get(user_id)):
        await update.effective_message.reply_text(
            f'{player}',
            disable_notification=silent
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
