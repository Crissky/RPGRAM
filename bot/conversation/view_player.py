'''
Arquivo responsável por gerenciar as requisiçães de visualização das 
informações dos jogadores.
'''

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)
from bot.conversation.constants import BASIC_COMMAND_FILTER, PREFIX_COMMANDS

from bot.conversation.sign_up_player import COMMANDS as sign_up_player_commands
from repository.mongo import PlayerModel


COMMANDS = ['jogador', 'player']


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    player_model = PlayerModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    print(f'{__name__}.start', 'chat.id:', chat_id)
    print(f'{__name__}.start', 'user_id:', user_id)

    if (player := player_model.get(user_id)):
        await update.effective_message.reply_text(f'{player}')
    else:
        await update.effective_message.reply_text(
            f'Você ainda não está cadastrado!\n'
            f'Cadastre-se com o comando /{sign_up_player_commands[0]}.'
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
