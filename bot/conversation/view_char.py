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

from bot.conversation.create_char import COMMANDS as create_char_commands
from bot.decorators import print_basic_infos
from repository.mongo import PlayerCharacterModel


COMMANDS = ['personagem', 'char']


@print_basic_infos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    player_char_model = PlayerCharacterModel()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    print(f'{__name__}.start', 'chat.id:', chat_id)
    print(f'{__name__}.start', 'user_id:', user_id)

    if (player_character := player_char_model.get(user_id)):
        await update.effective_message.reply_text(f'{player_character}')
    else:
        await update.effective_message.reply_text(
            f'Você ainda não criou um personagem!\n'
            f'Crie o seu personagem com o comando /{create_char_commands[0]}.'
        )

VIEW_CHAR_HANDLERS = [
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